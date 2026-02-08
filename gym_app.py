#!/usr/bin/env python3
"""
Gym App - Workout Plan Creator and Progress Tracker
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class Exercise:
    """Represents a single exercise"""
    
    def __init__(self, name: str, sets: int, reps: int, weight: Optional[float] = None):
        self.name = name
        self.sets = sets
        self.reps = reps
        self.weight = weight
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'sets': self.sets,
            'reps': self.reps,
            'weight': self.weight
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Exercise':
        return Exercise(
            name=data['name'],
            sets=data['sets'],
            reps=data['reps'],
            weight=data.get('weight')
        )
    
    def __str__(self) -> str:
        weight_str = f" @ {self.weight}kg" if self.weight else ""
        return f"{self.name}: {self.sets} sets x {self.reps} reps{weight_str}"


class Workout:
    """Represents a workout session"""
    
    def __init__(self, name: str, exercises: List[Exercise], day: Optional[str] = None):
        self.name = name
        self.exercises = exercises
        self.day = day
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'exercises': [ex.to_dict() for ex in self.exercises],
            'day': self.day
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Workout':
        return Workout(
            name=data['name'],
            exercises=[Exercise.from_dict(ex) for ex in data['exercises']],
            day=data.get('day')
        )
    
    def __str__(self) -> str:
        day_str = f" ({self.day})" if self.day else ""
        exercises_str = "\n  ".join(str(ex) for ex in self.exercises)
        return f"{self.name}{day_str}:\n  {exercises_str}"


class WorkoutPlan:
    """Represents a complete workout plan"""
    
    def __init__(self, name: str, workouts: List[Workout], description: str = ""):
        self.name = name
        self.workouts = workouts
        self.description = description
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'workouts': [w.to_dict() for w in self.workouts],
            'description': self.description,
            'created_at': self.created_at
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'WorkoutPlan':
        plan = WorkoutPlan(
            name=data['name'],
            workouts=[Workout.from_dict(w) for w in data['workouts']],
            description=data.get('description', '')
        )
        plan.created_at = data.get('created_at', datetime.now().isoformat())
        return plan


class ProgressEntry:
    """Represents a single progress entry"""
    
    def __init__(self, workout_name: str, date: str, exercises_completed: List[Dict], 
                 notes: str = ""):
        self.workout_name = workout_name
        self.date = date
        self.exercises_completed = exercises_completed
        self.notes = notes
    
    def to_dict(self) -> dict:
        return {
            'workout_name': self.workout_name,
            'date': self.date,
            'exercises_completed': self.exercises_completed,
            'notes': self.notes
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'ProgressEntry':
        return ProgressEntry(
            workout_name=data['workout_name'],
            date=data['date'],
            exercises_completed=data['exercises_completed'],
            notes=data.get('notes', '')
        )


class GymApp:
    """Main gym application for managing workout plans and tracking progress"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.plans_file = os.path.join(data_dir, "workout_plans.json")
        self.progress_file = os.path.join(data_dir, "progress.json")
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def _load_json(self, filepath: str) -> dict:
        """Load JSON data from file"""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_json(self, filepath: str, data: dict):
        """Save JSON data to file"""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    # Workout Plan Management
    def create_workout_plan(self, plan: WorkoutPlan) -> bool:
        """Create and save a new workout plan"""
        plans = self._load_json(self.plans_file)
        plans[plan.name] = plan.to_dict()
        self._save_json(self.plans_file, plans)
        return True
    
    def get_workout_plan(self, name: str) -> Optional[WorkoutPlan]:
        """Retrieve a workout plan by name"""
        plans = self._load_json(self.plans_file)
        if name in plans:
            return WorkoutPlan.from_dict(plans[name])
        return None
    
    def list_workout_plans(self) -> List[str]:
        """List all available workout plans"""
        plans = self._load_json(self.plans_file)
        return list(plans.keys())
    
    def delete_workout_plan(self, name: str) -> bool:
        """Delete a workout plan"""
        plans = self._load_json(self.plans_file)
        if name in plans:
            del plans[name]
            self._save_json(self.plans_file, plans)
            return True
        return False
    
    # Progress Tracking
    def log_progress(self, entry: ProgressEntry) -> bool:
        """Log a workout progress entry"""
        progress = self._load_json(self.progress_file)
        
        if 'entries' not in progress:
            progress['entries'] = []
        
        progress['entries'].append(entry.to_dict())
        self._save_json(self.progress_file, progress)
        return True
    
    def get_progress_history(self, workout_name: Optional[str] = None,
                            days: Optional[int] = None) -> List[ProgressEntry]:
        """Get progress history, optionally filtered by workout name and/or days"""
        progress = self._load_json(self.progress_file)
        entries = progress.get('entries', [])
        
        result = [ProgressEntry.from_dict(e) for e in entries]
        
        # Filter by workout name
        if workout_name:
            result = [e for e in result if e.workout_name == workout_name]
        
        # Filter by date range
        if days:
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            result = [e for e in result if e.date >= cutoff_date]
        
        return sorted(result, key=lambda x: x.date, reverse=True)
    
    def get_workout_stats(self, workout_name: str) -> Dict:
        """Get statistics for a specific workout"""
        entries = self.get_progress_history(workout_name=workout_name)
        
        return {
            'total_sessions': len(entries),
            'last_workout': entries[0].date if entries else None,
            'workout_name': workout_name
        }


def create_sample_plan() -> WorkoutPlan:
    """Create a sample workout plan for demonstration"""
    # Push Day
    push_exercises = [
        Exercise("Bench Press", 4, 8, 60),
        Exercise("Overhead Press", 3, 10, 40),
        Exercise("Incline Dumbbell Press", 3, 12, 20),
        Exercise("Tricep Dips", 3, 12),
        Exercise("Lateral Raises", 3, 15, 10)
    ]
    push_workout = Workout("Push Day", push_exercises, "Monday/Thursday")
    
    # Pull Day
    pull_exercises = [
        Exercise("Deadlift", 4, 6, 100),
        Exercise("Pull-ups", 3, 10),
        Exercise("Barbell Rows", 4, 8, 60),
        Exercise("Face Pulls", 3, 15, 15),
        Exercise("Bicep Curls", 3, 12, 15)
    ]
    pull_workout = Workout("Pull Day", pull_exercises, "Tuesday/Friday")
    
    # Leg Day
    leg_exercises = [
        Exercise("Squats", 4, 8, 80),
        Exercise("Romanian Deadlift", 3, 10, 60),
        Exercise("Leg Press", 3, 12, 100),
        Exercise("Leg Curls", 3, 12, 30),
        Exercise("Calf Raises", 4, 15, 40)
    ]
    leg_workout = Workout("Leg Day", leg_exercises, "Wednesday/Saturday")
    
    return WorkoutPlan(
        name="Push/Pull/Legs Split",
        workouts=[push_workout, pull_workout, leg_workout],
        description="A classic 6-day push/pull/legs training split for muscle building"
    )


def main():
    """Main CLI interface"""
    app = GymApp()
    
    print("=" * 60)
    print("GYM APP - Workout Plan Creator & Progress Tracker")
    print("=" * 60)
    print()
    
    while True:
        print("\nMain Menu:")
        print("1. Create/View Workout Plans")
        print("2. Log Workout Progress")
        print("3. View Progress History")
        print("4. View Workout Stats")
        print("5. Create Sample Plan")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            handle_workout_plans(app)
        elif choice == '2':
            handle_log_progress(app)
        elif choice == '3':
            handle_view_progress(app)
        elif choice == '4':
            handle_view_stats(app)
        elif choice == '5':
            handle_create_sample(app)
        elif choice == '6':
            print("\nGoodbye! Keep training hard! 💪")
            break
        else:
            print("\nInvalid choice. Please try again.")


def handle_workout_plans(app: GymApp):
    """Handle workout plan operations"""
    print("\n" + "=" * 60)
    print("WORKOUT PLANS")
    print("=" * 60)
    
    plans = app.list_workout_plans()
    if plans:
        print("\nAvailable Plans:")
        for i, plan_name in enumerate(plans, 1):
            print(f"{i}. {plan_name}")
        
        print("\nOptions:")
        print("- Enter plan number to view details")
        print("- Press Enter to go back")
        
        choice = input("\nYour choice: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(plans):
            plan_name = plans[int(choice) - 1]
            plan = app.get_workout_plan(plan_name)
            if plan:
                print(f"\n{'-' * 60}")
                print(f"Plan: {plan.name}")
                print(f"Description: {plan.description}")
                print(f"Created: {plan.created_at}")
                print(f"{'-' * 60}")
                for workout in plan.workouts:
                    print(f"\n{workout}")
    else:
        print("\nNo workout plans found. Create one using option 5 (Sample Plan) first!")


def handle_log_progress(app: GymApp):
    """Handle logging workout progress"""
    print("\n" + "=" * 60)
    print("LOG WORKOUT PROGRESS")
    print("=" * 60)
    
    plans = app.list_workout_plans()
    if not plans:
        print("\nNo workout plans available. Create a plan first!")
        return
    
    print("\nAvailable Workouts:")
    for i, plan_name in enumerate(plans, 1):
        plan = app.get_workout_plan(plan_name)
        if plan:
            for j, workout in enumerate(plan.workouts):
                print(f"{i}.{j+1}. {workout.name} (from {plan.name})")
    
    workout_name = input("\nEnter workout name: ").strip()
    if not workout_name:
        return
    
    exercises_completed = []
    print("\nLog exercises completed (press Enter with empty name to finish):")
    while True:
        ex_name = input("  Exercise name: ").strip()
        if not ex_name:
            break
        
        try:
            sets = int(input("  Sets completed: ").strip())
            reps = int(input("  Reps per set: ").strip())
            weight_str = input("  Weight (kg, press Enter to skip): ").strip()
            weight = float(weight_str) if weight_str else None
            
            exercises_completed.append({
                'name': ex_name,
                'sets': sets,
                'reps': reps,
                'weight': weight
            })
            print("  ✓ Exercise logged!")
        except ValueError:
            print("  ✗ Invalid input, skipping exercise")
    
    if exercises_completed:
        notes = input("\nAdditional notes (optional): ").strip()
        entry = ProgressEntry(
            workout_name=workout_name,
            date=datetime.now().isoformat(),
            exercises_completed=exercises_completed,
            notes=notes
        )
        app.log_progress(entry)
        print("\n✓ Progress logged successfully!")
    else:
        print("\nNo exercises logged.")


def handle_view_progress(app: GymApp):
    """Handle viewing progress history"""
    print("\n" + "=" * 60)
    print("PROGRESS HISTORY")
    print("=" * 60)
    
    days = input("\nShow last N days (press Enter for all): ").strip()
    days = int(days) if days.isdigit() else None
    
    entries = app.get_progress_history(days=days)
    
    if entries:
        print(f"\nFound {len(entries)} workout sessions:")
        print("-" * 60)
        for entry in entries:
            print(f"\nDate: {entry.date}")
            print(f"Workout: {entry.workout_name}")
            print("Exercises:")
            for ex in entry.exercises_completed:
                weight_str = f" @ {ex['weight']}kg" if ex.get('weight') else ""
                print(f"  - {ex['name']}: {ex['sets']}x{ex['reps']}{weight_str}")
            if entry.notes:
                print(f"Notes: {entry.notes}")
            print("-" * 60)
    else:
        print("\nNo progress entries found.")


def handle_view_stats(app: GymApp):
    """Handle viewing workout statistics"""
    print("\n" + "=" * 60)
    print("WORKOUT STATISTICS")
    print("=" * 60)
    
    workout_name = input("\nEnter workout name: ").strip()
    if not workout_name:
        return
    
    stats = app.get_workout_stats(workout_name)
    print(f"\nStats for '{workout_name}':")
    print(f"Total Sessions: {stats['total_sessions']}")
    print(f"Last Workout: {stats['last_workout'] or 'Never'}")


def handle_create_sample(app: GymApp):
    """Handle creating sample workout plan"""
    print("\n" + "=" * 60)
    print("CREATE SAMPLE PLAN")
    print("=" * 60)
    
    sample_plan = create_sample_plan()
    app.create_workout_plan(sample_plan)
    print(f"\n✓ Sample plan '{sample_plan.name}' created successfully!")
    print(f"\nPlan includes:")
    for workout in sample_plan.workouts:
        print(f"  - {workout.name} ({workout.day})")


if __name__ == "__main__":
    main()
