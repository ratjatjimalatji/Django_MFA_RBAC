from django.utils import timezone
from django.db.models import Count, Avg
from datetime import timedelta
from .models import RequestLog, Anomaly

class AnomalyDetector:
    """
    Simple rule-based anomaly detection system
    """
    
    def __init__(self):
        self.thresholds = {
            'error_rate_threshold': 0.3,  # 30% error rate
            'response_time_threshold': 5000,  # 5 seconds in milliseconds
            'requests_per_minute_threshold': 100,  # 100 requests per minute
            'consecutive_errors_threshold': 10,  # 10 consecutive errors
        }
    
    def detect_anomalies(self):
        """
        Run all anomaly detection algorithms
        """
        anomalies = []
        
        # Check for high error rates
        error_anomaly = self.detect_high_error_rate()
        if error_anomaly:
            anomalies.append(error_anomaly)
        
        # Check for slow response times
        slow_response_anomaly = self.detect_slow_responses()
        if slow_response_anomaly:
            anomalies.append(slow_response_anomaly)
        
        # Check for unusual traffic
        traffic_anomaly = self.detect_unusual_traffic()
        if traffic_anomaly:
            anomalies.append(traffic_anomaly)
        
        # Check for suspicious activity
        suspicious_anomaly = self.detect_suspicious_activity()
        if suspicious_anomaly:
            anomalies.append(suspicious_anomaly)
        
        return anomalies
    
    def detect_high_error_rate(self):
        """
        Detect if error rate in the last hour exceeds threshold
        """
        one_hour_ago = timezone.now() - timedelta(hours=1)
        
        # Get logs from the last hour
        recent_logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago)
        total_requests = recent_logs.count()
        
        if total_requests < 10:  # Not enough data
            return None
        
        # Count error responses (4xx and 5xx)
        error_logs = recent_logs.filter(status_code__gte=400)
        error_count = error_logs.count()
        
        error_rate = error_count / total_requests
        
        if error_rate > self.thresholds['error_rate_threshold']:
            # Check if this anomaly already exists
            existing_anomaly = Anomaly.objects.filter(
                anomaly_type='high_error_rate',
                detected_at__gte=one_hour_ago,
                is_resolved=False
            ).first()
            
            if not existing_anomaly:
                anomaly = Anomaly.objects.create(
                    anomaly_type='high_error_rate',
                    description=f'High error rate detected: {error_rate:.1%} ({error_count}/{total_requests} requests)',
                    severity='high' if error_rate > 0.5 else 'medium'
                )
                anomaly.related_logs.set(error_logs[:20])  # Add up to 20 related logs
                return anomaly
        
        return None
    
    def detect_slow_responses(self):
        """
        Detect if average response time in the last 30 minutes is too high
        """
        thirty_min_ago = timezone.now() - timedelta(minutes=30)
        
        # Get logs from the last 30 minutes
        recent_logs = RequestLog.objects.filter(timestamp__gte=thirty_min_ago)
        
        if recent_logs.count() < 5:  # Not enough data
            return None
        
        # Calculate average response time
        avg_response_time = recent_logs.aggregate(avg_time=Avg('response_time'))['avg_time']
        
        if avg_response_time and avg_response_time > self.thresholds['response_time_threshold']:
            # Check if this anomaly already exists
            existing_anomaly = Anomaly.objects.filter(
                anomaly_type='slow_response',
                detected_at__gte=thirty_min_ago,
                is_resolved=False
            ).first()
            
            if not existing_anomaly:
                slow_logs = recent_logs.filter(response_time__gt=self.thresholds['response_time_threshold'])
                
                anomaly = Anomaly.objects.create(
                    anomaly_type='slow_response',
                    description=f'Slow response times detected: {avg_response_time:.0f}ms average (threshold: {self.thresholds["response_time_threshold"]}ms)',
                    severity='medium' if avg_response_time < 10000 else 'high'
                )
                anomaly.related_logs.set(slow_logs[:10])
                return anomaly
        
        return None
    
    def detect_unusual_traffic(self):
        """
        Detect unusual traffic spikes
        """
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        
        # Count requests in the last minute
        recent_requests = RequestLog.objects.filter(timestamp__gte=one_minute_ago).count()
        
        if recent_requests > self.thresholds['requests_per_minute_threshold']:
            # Check if this anomaly already exists
            existing_anomaly = Anomaly.objects.filter(
                anomaly_type='unusual_traffic',
                detected_at__gte=one_minute_ago,
                is_resolved=False
            ).first()
            
            if not existing_anomaly:
                recent_logs = RequestLog.objects.filter(timestamp__gte=one_minute_ago)
                
                anomaly = Anomaly.objects.create(
                    anomaly_type='unusual_traffic',
                    description=f'Unusual traffic spike: {recent_requests} requests in the last minute (threshold: {self.thresholds["requests_per_minute_threshold"]})',
                    severity='high' if recent_requests > 200 else 'medium'
                )
                anomaly.related_logs.set(recent_logs[:20])
                return anomaly
        
        return None
    
    def detect_suspicious_activity(self):
        """
        Detect consecutive errors from the same IP (possible attack)
        """
        ten_min_ago = timezone.now() - timedelta(minutes=10)
        
        # Get recent error logs
        error_logs = RequestLog.objects.filter(
            timestamp__gte=ten_min_ago,
            status_code__gte=400
        ).order_by('ip_address', 'timestamp')
        
        # Group by IP and count consecutive errors
        ip_error_counts = {}
        for log in error_logs:
            if log.ip_address:
                if log.ip_address not in ip_error_counts:
                    ip_error_counts[log.ip_address] = 0
                ip_error_counts[log.ip_address] += 1
        
        # Find IPs with too many errors
        for ip, count in ip_error_counts.items():
            if count >= self.thresholds['consecutive_errors_threshold']:
                # Check if this anomaly already exists for this IP
                existing_anomaly = Anomaly.objects.filter(
                    anomaly_type='suspicious_activity',
                    description__contains=ip,
                    detected_at__gte=ten_min_ago,
                    is_resolved=False
                ).first()
                
                if not existing_anomaly:
                    suspicious_logs = RequestLog.objects.filter(
                        timestamp__gte=ten_min_ago,
                        ip_address=ip,
                        status_code__gte=400
                    )
                    
                    anomaly = Anomaly.objects.create(
                        anomaly_type='suspicious_activity',
                        description=f'Suspicious activity from IP {ip}: {count} consecutive errors in 10 minutes',
                        severity='high' if count > 20 else 'medium'
                    )
                    anomaly.related_logs.set(suspicious_logs)
                    return anomaly
        
        return None
    
    def resolve_anomaly(self, anomaly_id):
        """
        Mark an anomaly as resolved
        """
        try:
            anomaly = Anomaly.objects.get(id=anomaly_id)
            anomaly.is_resolved = True
            anomaly.save()
            return True
        except Anomaly.DoesNotExist:
            return False