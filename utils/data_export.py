#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


class DataExporter:
    def __init__(self, results_dir: str = "results"):
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(exist_ok=True)

    def save_user_data(self, user_data: Dict[str, Any], chat_id: int) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"user_{user_data['id']}_{chat_id}_{timestamp}.json"
        filepath = self.results_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, ensure_ascii=False, indent=2)

        return str(filepath)

    def save_batch_data(self, users_data: List[Dict[str, Any]], chat_info: Dict[str, Any]) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_{chat_info['chat_id']}_members_{timestamp}.json"
        filepath = self.results_dir / filename

        result_data = {
            'chat_name': chat_info.get('chat_name', 'Unknown'),
            'chat_id': chat_info['chat_id'],
            'parsing_mode': chat_info.get('mode', 'members'),
            'members_count': len(users_data),
            'extraction_date': datetime.now().isoformat(),
            'parameters': chat_info.get('parameters', {}),
            'members': users_data
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)

        return str(filepath)
