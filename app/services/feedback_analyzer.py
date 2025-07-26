import openai
import re
import json
from typing import List, Dict, Any
from collections import Counter
from app.core.config import settings
from app.models.feedback import FeedbackReport, WeakAnswer, FillerWordAnalysis, ConfidenceMarker

class FeedbackAnalyzer:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.filler_words = [
            "um", "uh", "like", "you know", "so", "basically", "actually", 
            "literally", "kinda", "sorta", "well", "right", "okay"
        ]
        self.confidence_hedges = [
            "i think", "maybe", "probably", "i guess", "sort of", "kind of",
            "i'm not sure", "perhaps", "i believe", "it seems"
        ]
    
    def analyze_filler_words(self, transcript: str, segments: List[Dict]) -> List[FillerWordAnalysis]:
        """Analyze filler word usage"""
        filler_analysis = []
        words = transcript.lower().split()
        
        for filler in self.filler_words:
            count = words.count(filler)
            if count > 0:
                timestamps = []
                # Extract timestamps from segments if available
                for segment in segments:
                    segment_words = segment.get('text', '').lower().split()
                    if filler in segment_words:
                        timestamps.append(segment.get('start', 0))
                
                filler_analysis.append(FillerWordAnalysis(
                    word=filler,
                    count=count,
                    timestamps=timestamps
                ))
        
        return sorted(filler_analysis, key=lambda x: x.count, reverse=True)
    
    def analyze_confidence_markers(self, transcript: str) -> List[ConfidenceMarker]:
        """Analyze confidence markers and hedging language"""
        markers = []
        transcript_lower = transcript.lower()
        
        hedge_count = sum(1 for hedge in self.confidence_hedges if hedge in transcript_lower)
        if hedge_count > 3:
            markers.append(ConfidenceMarker(
                marker_type="hedging_language",
                examples=[hedge for hedge in self.confidence_hedges if hedge in transcript_lower][:3],
                impact="Reduces perceived confidence and authority",
                suggestion="Replace hedging language with definitive statements when appropriate"
            ))
        
        # Check for upspeak patterns (questions ending statements)
        question_patterns = len(re.findall(r'[.]\s*[A-Z][^.]*\?', transcript))
        if question_patterns > 2:
            markers.append(ConfidenceMarker(
                marker_type="upspeak",
                examples=["Statements ending with rising intonation"],
                impact="Makes statements sound like questions, reducing authority",
                suggestion="Practice ending statements with falling intonation"
            ))
        
        return markers
    
    def detect_jargon(self, transcript: str) -> List[str]:
        """Detect overuse of technical jargon"""
        jargon_words = [
            "synergy", "leverage", "paradigm", "ecosystem", "scalable", "disruptive",
            "innovative", "cutting-edge", "best practices", "core competencies",
            "value-added", "holistic", "proactive", "streamline"
        ]
        
        found_jargon = []
        transcript_lower = transcript.lower()
        
        for word in jargon_words:
            if word in transcript_lower:
                count = transcript_lower.count(word)
                if count >= 2:
                    found_jargon.append(f"{word} (used {count} times)")
        
        return found_jargon
    
    async def analyze_content_with_gpt(self, transcript: str) -> Dict[str, Any]:
        """Use GPT to analyze interview content and provide feedback"""
        prompt = f"""
        Analyze this interview transcript and provide structured feedback:

        TRANSCRIPT:
        {transcript}

        Please provide:
        1. Overall performance score (1-10)
        2. Identify 2-3 weak answers with specific issues
        3. Suggest improvements for each weak answer
        4. Provide 3-5 actionable recommendations

        Format your response as JSON with the following structure:
        {{
            "overall_score": 7.5,
            "weak_answers": [
                {{
                    "question": "inferred question",
                    "original_answer": "excerpt from transcript",
                    "issues": ["issue1", "issue2"],
                    "suggestions": ["suggestion1", "suggestion2"],
                    "improved_example": "better answer example"
                }}
            ],
            "recommendations": ["rec1", "rec2", "rec3"]
        }}
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=settings.GPT_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            print(f"Error analyzing with GPT: {e}")
            return {
                "overall_score": 5.0,
                "weak_answers": [],
                "recommendations": ["Unable to generate detailed feedback at this time"]
            }
    
    async def generate_feedback_report(self, transcript: str, segments: List[Dict], interview_id: str) -> FeedbackReport:
        """Generate comprehensive feedback report"""
        
        # Analyze different aspects
        filler_words = self.analyze_filler_words(transcript, segments)
        confidence_markers = self.analyze_confidence_markers(transcript)
        jargon_usage = self.detect_jargon(transcript)
        gpt_analysis = await self.analyze_content_with_gpt(transcript)
        
        # Parse GPT analysis
        weak_answers = [
            WeakAnswer(**answer) for answer in gpt_analysis.get("weak_answers", [])
        ]
        
        return FeedbackReport(
            interview_id=interview_id,
            transcript=transcript,
            overall_score=gpt_analysis.get("overall_score", 5.0),
            weak_answers=weak_answers,
            filler_words=filler_words,
            confidence_markers=confidence_markers,
            jargon_usage=jargon_usage,
            recommendations=gpt_analysis.get("recommendations", [])
        )

