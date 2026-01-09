import requests
from typing import List, Optional, Dict
from config import API_BASE_URL, API_TIMEOUT, MAX_RETRIES
import time

class TelegramAPIClient:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.timeout = API_TIMEOUT
    
    def _make_request(self, method: str, endpoint: str, 
                      data: dict = None, retries: int = MAX_RETRIES) -> dict:
        """Make HTTP request with retry logic"""
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(retries):
            try:
                if method.upper() == 'GET':
                    response = self.session.get(url, params=data)
                else:
                    response = self.session.post(url, json=data)
                
                response.raise_for_status()
                return response.json()
            
            except requests.exceptions.Timeout:
                if attempt == retries - 1:
                    raise Exception("Request timed out after multiple retries")
                time.sleep(2 ** attempt)
            
            except requests.exceptions.ConnectionError:
                if attempt == retries - 1:
                    raise Exception("Could not connect to API server")
                time.sleep(2 ** attempt)
            
            except requests.exceptions.HTTPError as e:
                if e.response.status_code >= 500:
                    if attempt == retries - 1:
                        raise Exception(f"Server error: {e.response.status_code}")
                    time.sleep(2 ** attempt)
                else:
                    # Client error, don't retry
                    try:
                        error_detail = e.response.json().get('detail', str(e))
                    except:
                        error_detail = str(e)
                    raise Exception(f"API error: {error_detail}")
            
            except Exception as e:
                raise Exception(f"Unexpected error: {str(e)}")
    
    # Health endpoints
    def get_health(self) -> dict:
        """Get API health status"""
        return self._make_request('GET', '/health')
    
    def ping(self) -> dict:
        """Ping API"""
        return self._make_request('GET', '/ping')
    
    # Account endpoints
    def get_accounts_status(self) -> dict:
        """Get status of all accounts"""
        return self._make_request('GET', '/accounts/status')
    
    def authorize_account(self, phone: str, code: str = None, 
                         password: str = None) -> dict:
        """Authorize a Telegram account"""
        data = {'phone': phone}
        if code:
            data['code'] = code
        if password:
            data['password'] = password
        
        return self._make_request('POST', '/accounts/authorize', data)
    
    def reactivate_accounts(self, phones: List[str]) -> dict:
        """Reactivate inactive accounts"""
        return self._make_request('POST', '/accounts/reactivate', {'phones': phones})
    
    # Message endpoints
    def send_message(self, target: str, message: str, 
                    phones: List[str] = None, account_count: int = None) -> dict:
        """Send message to a user/channel"""
        data = {
            'target': target,
            'message': message
        }
        if phones:
            data['phones'] = phones
        if account_count:
            data['account_count'] = account_count
        
        return self._make_request('POST', '/messages/send', data)
    
    # Channel endpoints
    def create_channels(self, title: str, about: str, is_public: bool,
                       phones: List[str] = None, account_count: int = None) -> dict:
        """Create channels"""
        data = {
            'title': title,
            'about': about,
            'is_public': is_public
        }
        if phones:
            data['phones'] = phones
        if account_count:
            data['account_count'] = account_count
        
        return self._make_request('POST', '/channels/create', data)
    
    def join_channels(self, channels: List[str], 
                     phones: List[str] = None, account_count: int = None) -> dict:
        """Join channels"""
        data = {'channels': channels}
        if phones:
            data['phones'] = phones
        if account_count:
            data['account_count'] = account_count
        
        return self._make_request('POST', '/channels/join', data)
    
    def view_posts(self, channel: str, limit: int,
                  phones: List[str] = None, account_count: int = None) -> dict:
        """View channel posts"""
        data = {
            'channel': channel,
            'limit': limit
        }
        if phones:
            data['phones'] = phones
        if account_count:
            data['account_count'] = account_count
        
        return self._make_request('POST', '/channels/posts/view', data)
    
    # Group endpoints
    def create_groups(self, title: str, about: str,
                     phones: List[str] = None, account_count: int = None) -> dict:
        """Create groups"""
        data = {
            'title': title,
            'about': about
        }
        if phones:
            data['phones'] = phones
        if account_count:
            data['account_count'] = account_count
        
        return self._make_request('POST', '/groups/create', data)
    
    # Bot endpoints
    def create_bots(self, bot_name: str, bot_username: str,
                   phones: List[str] = None, account_count: int = None) -> dict:
        """Create bots"""
        data = {
            'bot_name': bot_name,
            'bot_username': bot_username
        }
        if phones:
            data['phones'] = phones
        if account_count:
            data['account_count'] = account_count
        
        return self._make_request('POST', '/bots/create', data)
    
    # Report endpoints
    def send_report(self, targets: List[str], reason: str,
                   phones: List[str] = None, account_count: int = None) -> dict:
        """Send reports"""
        data = {
            'targets': targets,
            'reason': reason
        }
        if phones:
            data['phones'] = phones
        if account_count:
            data['account_count'] = account_count
        
        return self._make_request('POST', '/reports/send', data)
    
    def start_continuous_report(self, targets: List[str], reason: str, 
                               interval: int, phones: List[str] = None,
                               account_count: int = None, start_time: str = None) -> dict:
        """Start continuous reporting campaign"""
        data = {
            'targets': targets,
            'reason': reason,
            'interval': interval
        }
        if phones:
            data['phones'] = phones
        if account_count:
            data['account_count'] = account_count
        if start_time:
            data['start_time'] = start_time
        
        return self._make_request('POST', '/reports/continuous/start', data)
    
    def stop_continuous_report(self, task_id: str) -> dict:
        """Stop continuous reporting campaign"""
        return self._make_request('POST', f'/reports/continuous/stop/{task_id}')
    
    # Reaction endpoints
    def send_reactions(self, channel: str, message_ids: List[int], reaction: str,
                      phones: List[str] = None, account_count: int = None) -> dict:
        """Send reactions to messages"""
        data = {
            'channel': channel,
            'message_ids': message_ids,
            'reaction': reaction
        }
        if phones:
            data['phones'] = phones
        if account_count:
            data['account_count'] = account_count
        
        return self._make_request('POST', '/reactions/send', data)
    
    # Forward endpoints
    def forward_messages(self, from_channel: str, to_channels: List[str],
                        message_ids: List[int], phones: List[str] = None,
                        account_count: int = None) -> dict:
        """Forward messages"""
        data = {
            'from_channel': from_channel,
            'to_channels': to_channels,
            'message_ids': message_ids
        }
        if phones:
            data['phones'] = phones
        if account_count:
            data['account_count'] = account_count
        
        return self._make_request('POST', '/forwards/messages', data)
    
    # Task endpoints
    def get_all_tasks(self) -> dict:
        """Get all tasks"""
        return self._make_request('GET', '/tasks')
    
    def get_task(self, task_id: str) -> dict:
        """Get specific task details"""
        return self._make_request('GET', f'/tasks/{task_id}')
    
    def cancel_task(self, task_id: str) -> dict:
        """Cancel a task"""
        return self._make_request('POST', f'/tasks/{task_id}/cancel')
