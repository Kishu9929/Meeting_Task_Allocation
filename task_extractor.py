"""
Custom task extraction logic from transcribed text
"""
import re
from typing import List, Dict, Optional
from config import TEAM_MEMBERS, PRIORITY_KEYWORDS, DEADLINE_PATTERNS


class TaskExtractor:
    def __init__(self):
        self.team_members = TEAM_MEMBERS
        self.priority_keywords = PRIORITY_KEYWORDS
        self.deadline_patterns = DEADLINE_PATTERNS
    
    def extract_tasks(self, text: str) -> List[Dict]:
        """
        Extract tasks from transcribed text
        
        Args:
            text: Transcribed meeting text
            
        Returns:
            List of task dictionaries
        """
        original_text = text
        text_lower = text.lower()
        
        sentences = re.split(r'[.!?]\s+', text)
        original_sentences = re.split(r'[.!?]\s+', original_text)
        
        tasks = []
        task_id = 1
        
        task_indicators = [
            r"need\s+(?:to\s+|someone\s+to\s+)",
            r"we\s+need\s+(?:to\s+|someone\s+to\s+)",
            r"should\s+",
            r"must\s+",
            r"have\s+to\s+",
            r"required\s+to\s+",
            r"someone\s+should\s+",
            r"tackle\s+",
            r"update\s+",
            r"write\s+",
            r"design\s+",
            r"fix\s+",
            r"optimize\s+",
        ]
        
        i = 0
        while i < len(sentences):
            sentence = sentences[i].strip()
            original_sentence = original_sentences[i].strip() if i < len(original_sentences) else sentence
            
            if not sentence:
                i += 1
                continue
            
            is_task_sentence = any(re.search(indicator, sentence) for indicator in task_indicators)
            
            if is_task_sentence:
                context_parts = []
                context_original_parts = []
                
                if i > 0:
                    prev_sentence = sentences[i - 1].strip()
                    prev_original = original_sentences[i - 1].strip() if i - 1 < len(original_sentences) else prev_sentence
                    if prev_sentence:
                        context_parts.append(prev_sentence)
                        context_original_parts.append(prev_original)
                
                context_parts.append(sentence)
                context_original_parts.append(original_sentence)
                
                if i + 1 < len(sentences):
                    next_sentence = sentences[i + 1].strip()
                    next_original = original_sentences[i + 1].strip() if i + 1 < len(original_sentences) else next_sentence
                    if any(word in next_sentence for word in ["by", "before", "end", "priority", "depends", "since", "understand"]):
                        context_parts.append(next_sentence)
                        context_original_parts.append(next_original)
                        i += 1  
                
                full_context = ". ".join(context_parts)
                full_context_original = ". ".join(context_original_parts)

                task_desc = self._extract_task_description(full_context, full_context_original)
                
                if task_desc:
                    assignee = self._extract_assignee(full_context, full_context_original, text_lower, original_text)
                    
                    deadline = self._extract_deadline(full_context)
                    
                    priority = self._extract_priority(full_context)
                    
                    dependencies = self._extract_dependencies(full_context, task_id, tasks)
                    
                    reason = self._extract_reason(full_context, assignee)
                    
                    task = {
                        "id": task_id,
                        "task": task_desc,
                        "assigned_to": assignee or "Unassigned",
                        "deadline": deadline or "Not specified",
                        "priority": priority or "Medium",
                        "dependencies": dependencies or "",
                        "reason": reason or ""
                    }
                    tasks.append(task)
                    task_id += 1
            
            i += 1
        
        return tasks
    
    def _extract_task_description(self, sentence: str, original_sentence: str = None) -> Optional[str]:
        """Extract the task description from a sentence"""
        if original_sentence is None:
            original_sentence = sentence
        
        prefixes = [
            r"^(hi\s+everyone[,\s]+)",
            r"^(let'?s\s+)",
            r"^(also[,\s]+)",
            r"^(and\s+)",
            r"^(oh\s+and\s+)",
            r"^(one\s+more\s+thing[,\s]+)",
        ]
        
        cleaned = sentence
        for prefix in prefixes:
            cleaned = re.sub(prefix, "", cleaned, flags=re.IGNORECASE)
        
        patterns = [
            r"(?:we\s+)?need\s+(?:to\s+|someone\s+to\s+)(.+?)(?:\.|,|since|that|this|$)",
            r"should\s+(?:tackle|fix|update|write|design|optimize)\s+(.+?)(?:\.|,|by|before|$)",
            r"must\s+(.+?)(?:\.|,|$)",
            r"have\s+to\s+(.+?)(?:\.|,|$)",
            r"required\s+to\s+(.+?)(?:\.|,|$)",
            r"someone\s+should\s+(.+?)(?:\.|,|$)",
            r"tackle\s+(.+?)(?:\.|,|by|before|$)",
            r"update\s+(.+?)(?:\.|,|by|before|$)",
            r"write\s+(.+?)(?:\.|,|by|before|$)",
            r"design\s+(.+?)(?:\.|,|by|before|$)",
            r"fix\s+(.+?)(?:\.|,|by|before|$)",
            r"optimize\s+(.+?)(?:\.|,|by|before|$)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, cleaned, re.IGNORECASE)
            if match:
                desc = match.group(1).strip()
                desc = re.sub(r"\s+(?:since|that|this|it'?s|which).*$", "", desc, flags=re.IGNORECASE)
                desc = re.sub(r"\s+", " ", desc)
                if desc:
                    desc = desc[0].upper() + desc[1:] if len(desc) > 1 else desc.upper()
                return desc
        
        return None
    
    def _extract_assignee(self, sentence: str, original_sentence: str = None, full_text: str = None, full_text_original: str = None) -> Optional[str]:
        """
        Extract assignee name from sentence with priority on explicit mentions.
        Uses custom logic only (regex, pattern matching) - no external APIs or pre-trained models.
        """
        if original_sentence is None:
            original_sentence = sentence
        if full_text_original is None:
            full_text_original = full_text if full_text else sentence
        
        sentence_lower = sentence.lower()
        
        name_variations = {
            "Sakshi": ["sakshi", "saksh", "sakshy", "sakshie", "saksh", "sakshy", "sakshie", 
                      "sakshi", "saksh", "sakshy", "sakshie", "saksh", "sakshy"],
            "Mohit": ["mohit", "moheet", "moheeth", "mohith", "moeeth", "mohit", "moheet", "mohit"],
            "Arjun": ["arjun", "arjunn", "arjune", "arjuan", "arjun"],
            "Lata": ["lata", "latha", "lataa", "lata"]
        }
        
        for member in self.team_members:
            name = member["name"]
            name_lower = name.lower()
            
            if name in original_sentence:
                return name
            
            if name_lower in sentence_lower:
                return name
            
            if name in name_variations:
                for variation in name_variations[name]:
                    pattern = rf"\b{re.escape(variation)}\b"
                    if re.search(pattern, sentence_lower):
                        return name
        
        for member in self.team_members:
            name = member["name"]
            name_lower = name.lower()
            patterns = [
                rf"{re.escape(name_lower)}\s*[,]?\s*(?:we\s+need|you'?re|you\s+are|can\s+you)",
                rf"{re.escape(name_lower)}\s*[,]?\s+(?:please|will\s+you)",
            ]
            for pattern in patterns:
                if re.search(pattern, sentence_lower):
                    return name

        test_patterns = [
            r"write\s+(?:unit\s+)?test",
            r"write\s+(?:unit\s+)?tests",
            r"create\s+(?:unit\s+)?test",
            r"develop\s+(?:unit\s+)?test"
        ]
        for pattern in test_patterns:
            if re.search(pattern, sentence_lower, re.IGNORECASE):
                return "Lata" 
        
        if re.search(r"\bapi\s+documentation\b", sentence_lower, re.IGNORECASE):
            return "Mohit"  
        
        if re.search(r"\b(?:update|write|create)\s+.*\s+documentation\b", sentence_lower, re.IGNORECASE):
            return "Mohit"  
        
        else:
            design_keywords = [
                r"design\s+\w+",
                r"design\s+new",
                r"design\s+the",
                r"onboarding\s+screens",
                r"new\s+onboarding",
                r"ui\s+design",
                r"ux\s+design",
                r"user\s+interface",
                r"user\s+experience",
                r"screen\s+design",
                r"design\s+screens"
            ]
            for pattern in design_keywords:
                if re.search(pattern, sentence_lower, re.IGNORECASE):
                    return "Arjun" 
            
            if re.search(r"\b(?:design|onboarding|screens)\b", sentence_lower, re.IGNORECASE):
                return "Arjun"  
            
            ui_ux_match = re.search(r"\b(ui|ux)\b", sentence_lower, re.IGNORECASE)
            if ui_ux_match:
                match_pos = ui_ux_match.start()
                if match_pos >= 3:
                    before_text = sentence_lower[max(0, match_pos-3):match_pos]
                    if "api" not in before_text:
                        return "Arjun"  
                else:
                    return "Arjun"  
        
        if full_text and full_text_original:
            full_text_lower = full_text.lower()
            sentence_lower_clean = sentence_lower.strip()

            sentence_pos = -1
            first_words = " ".join(sentence_lower_clean.split()[:3])
            if first_words:
                sentence_pos = full_text_lower.find(first_words)
            
            if sentence_pos >= 0:
                context_start = max(0, sentence_pos - 400)
                context_end = min(len(full_text_lower), sentence_pos + len(sentence_lower_clean) + 100)
                context = full_text_lower[context_start:context_end]
                context_original = full_text_original[context_start:context_end]

                for member in self.team_members:
                    name = member["name"]
                    name_lower = name.lower()
                    
                    if name in context_original:
                        pattern = rf"\b{re.escape(name)}\b"
                        if re.search(pattern, context_original):
                            return name
                    
                    if name_lower in context:
                        pattern = rf"\b{re.escape(name_lower)}\b"
                        if re.search(pattern, context):
                            return name

                    if name in name_variations:
                        for variation in name_variations[name]:
                            pattern = rf"\b{re.escape(variation)}\b"
                            if re.search(pattern, context):
                                return name
        

        context_lower = sentence_lower
        
        test_patterns = [
            r"write\s+(?:unit\s+)?test",
            r"write\s+(?:unit\s+)?tests",
            r"create\s+(?:unit\s+)?test",
            r"develop\s+(?:unit\s+)?test"
        ]
        
        for pattern in test_patterns:
            if re.search(pattern, context_lower, re.IGNORECASE):
                return "Lata"  

        if full_text:
            full_text_lower = full_text.lower()
            for pattern in test_patterns:
                if re.search(pattern, full_text_lower, re.IGNORECASE):
                    return "Lata"  
        
        testing_phrases = [
            r"unit\s+test",
            r"unit\s+tests",
            r"write\s+tests",
            r"test\s+for\s+\w+\s+module",
            r"test\s+the\s+\w+\s+module",
            r"qa\s+test",
            r"quality\s+assurance",
            r"automation\s+test",
            r"test\s+module",
            r"testing\s+task",
            r"create\s+test",
            r"develop\s+test"
        ]
        
        for pattern in testing_phrases:
            if re.search(pattern, context_lower, re.IGNORECASE):
                return "Lata" 
            
        role_patterns = {
            "frontend": "Sakshi",
            "backend": "Mohit",
            "api documentation": "Mohit",  
            "api doc": "Mohit",
            "documentation": "Mohit",  
            "ui": "Arjun",
            "ux": "Arjun",
            "design": "Arjun",
            "qa": "Lata",
            "test": "Lata",
            "testing": "Lata"
        }
        
        if re.search(r"\bapi\s+documentation\b", context_lower, re.IGNORECASE):
            return "Mohit"  
        
        for role_keyword, default_assignee in role_patterns.items():
            pattern = rf"\b{re.escape(role_keyword)}\b"
            if re.search(pattern, context_lower, re.IGNORECASE):
                if role_keyword == "ui" and re.search(r"\bapi\b", context_lower, re.IGNORECASE):
                    continue
                return default_assignee
        
        skill_matches = []
        for member in self.team_members:
            for skill in member["skills"]:
                skill_lower = skill.lower()
                pattern = rf"\b{re.escape(skill_lower)}\b"
                if re.search(pattern, context_lower, re.IGNORECASE):
                    skill_matches.append((len(skill_lower), member["name"]))  
        
        if skill_matches:
            skill_matches.sort(reverse=True)  
            return skill_matches[0][1]
        
        return None
    
    def _extract_deadline(self, sentence: str) -> Optional[str]:
        """Extract deadline from sentence using custom pattern matching"""
        sentence_lower = sentence.lower()
        
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        
        for day in days:
            patterns = [
                rf"till\s+(?:next\s+)?{day}",
                rf"until\s+(?:next\s+)?{day}",
                rf"by\s+(?:next\s+)?{day}",
                rf"till\s+{day}",
                rf"until\s+{day}",
            ]
            for pattern in patterns:
                match = re.search(pattern, sentence_lower)
                if match:
                    matched_text = match.group(0)
                    parts = matched_text.split()
                    if "next" in parts:
                        day_name = parts[-1].capitalize()
                        return f"Next {day_name}"
                    else:
                        return day.capitalize()
        
        if "tomorrow evening" in sentence_lower or "by tomorrow evening" in sentence_lower:
            return "Tomorrow evening"
        elif "next monday" in sentence_lower:
            return "Next Monday"
        elif "tomorrow" in sentence_lower:
            return "Tomorrow"
        elif "end of this week" in sentence_lower:
            return "End of this week"
        elif "end of the week" in sentence_lower:
            return "End of this week"
        elif "before friday" in sentence_lower:
            return "Friday"
        elif "friday" in sentence_lower:
            return "Friday"
        elif "wednesday" in sentence_lower:
            return "Wednesday"
        elif "monday" in sentence_lower:
            return "Monday"
        elif "tuesday" in sentence_lower:
            return "Tuesday"
        elif "thursday" in sentence_lower:
            return "Thursday"
        elif "saturday" in sentence_lower:
            return "Saturday"
        elif "sunday" in sentence_lower:
            return "Sunday"
        
        # Try regex patterns from config
        for pattern in self.deadline_patterns:
            match = re.search(pattern, sentence_lower)
            if match:
                deadline_text = match.group(0)
                # Capitalize properly
                if len(deadline_text) > 1:
                    deadline_text = deadline_text[0].upper() + deadline_text[1:]
                else:
                    deadline_text = deadline_text.upper()
                return deadline_text
        
        return None
    
    def _extract_priority(self, sentence: str) -> Optional[str]:
        """Extract priority from sentence"""
        sentence_lower = sentence.lower()
        
        # Check priority keywords in order of importance
        for priority_level in ["critical", "high", "medium", "low"]:
            keywords = self.priority_keywords[priority_level]
            for keyword in keywords:
                if keyword in sentence_lower:
                    return priority_level.capitalize()
        
        # Default priority based on keywords
        if "blocking" in sentence_lower or "urgent" in sentence_lower:
            return "Critical"
        elif "high priority" in sentence_lower or "important" in sentence_lower:
            return "High"
        elif "can wait" in sentence_lower:
            return "Medium"
        
        return "Medium"  # Default
    
    def _extract_dependencies(self, sentence: str, current_task_id: int, existing_tasks: List[Dict] = None) -> Optional[str]:
        """Extract task dependencies"""
        if existing_tasks is None:
            existing_tasks = []
        
        sentence_lower = sentence.lower()
        
        dependency_keywords = [
            r"depends?\s+on",
            r"after\s+",
            r"following\s+",
            r"once\s+",
        ]
        
        for keyword in dependency_keywords:
            if re.search(keyword, sentence_lower):
                # Try to find task number
                task_num_match = re.search(r"task\s*#?(\d+)", sentence_lower)
                if task_num_match:
                    return f"Depends on Task #{task_num_match.group(1)}"
                
                # Try to find task description and match to existing tasks
                if "login bug" in sentence_lower or "bug fix" in sentence_lower or "login" in sentence_lower:
                    # Find the login bug task
                    for task in existing_tasks:
                        if "login" in task.get("task", "").lower() or "bug" in task.get("task", "").lower():
                            return f"Depends on Task #{task['id']}"
                    return "Depends on Task #1"
                
                return "Has dependencies"
        
        return None
    
    def _extract_reason(self, sentence: str, assignee: Optional[str]) -> Optional[str]:
        """Extract reason for assignment"""
        reasons = []
        
        if assignee:
            # Find role-based reasons
            for member in self.team_members:
                if member["name"] == assignee:
                    role = member["role"].lower()
                    if "frontend" in role:
                        reasons.append("Frontend task")
                    elif "backend" in role:
                        reasons.append("Backend expertise")
                    elif "design" in role or "ui" in role or "ux" in role:
                        reasons.append("UI/UX task")
                    elif "qa" in role or "test" in role:
                        reasons.append("QA expertise")
                    break
        
        # Check for specific reasons in sentence
        sentence_lower = sentence.lower()
        if "blocking" in sentence_lower or "blocking users" in sentence_lower:
            reasons.append("blocking users")
        if "relevant experience" in sentence_lower or "worked on" in sentence_lower:
            reasons.append("relevant experience")
        if "testing task" in sentence_lower or "test" in sentence_lower:
            reasons.append("testing task")
        
        return ", ".join(reasons) if reasons else None

