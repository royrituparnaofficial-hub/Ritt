#!/usr/bin/env python3
"""
Demo script to showcase the Gym App features
"""

from gym_app import Exercise, Workout, WorkoutPlan, ProgressEntry, GymApp
from datetime import datetime, timedelta

def demo():
    """Run a complete demo of the gym app"""
    print("=" * 70)
    print("GYM APP DEMO - Workout Plan Creator & Progress Tracker")
    print("=" * 70)
    print()
    
    # Initialize app
    app = GymApp()
    
    # Demo 1: Create a custom workout plan
    print("📋 DEMO 1: Creating a Custom Workout Plan")
    print("-" * 70)
    
    exercises = [
        Exercise("Barbell Squat", 4, 10, 100),
        Exercise("Leg Press", 3, 12, 150),
        Exercise("Leg Curls", 3, 15, 40),
        Exercise("Calf Raises", 4, 20, 50)
    ]
    leg_workout = Workout("Leg Day", exercises, "Wednesday")
    
    plan = WorkoutPlan(
        name="Custom Leg Program",
        workouts=[leg_workout],
        description="Focused leg strength and hypertrophy program"
    )
    
    app.create_workout_plan(plan)
    print(f"✓ Created workout plan: {plan.name}")
    print(f"  Description: {plan.description}")
    print(f"  Workouts: {len(plan.workouts)}")
    print()
    
    # Demo 2: View workout plans
    print("📖 DEMO 2: Viewing All Workout Plans")
    print("-" * 70)
    
    plans = app.list_workout_plans()
    print(f"Found {len(plans)} workout plan(s):")
    for i, plan_name in enumerate(plans, 1):
        retrieved_plan = app.get_workout_plan(plan_name)
        print(f"\n{i}. {plan_name}")
        if retrieved_plan:
            for workout in retrieved_plan.workouts:
                print(f"   - {workout.name}: {len(workout.exercises)} exercises")
    print()
    
    # Demo 3: Log progress
    print("📝 DEMO 3: Logging Workout Progress")
    print("-" * 70)
    
    # Simulate 3 workout sessions
    for i in range(3):
        date = (datetime.now() - timedelta(days=6-i*2)).isoformat()
        exercises_done = [
            {'name': 'Barbell Squat', 'sets': 4, 'reps': 10, 'weight': 100 + i*5},
            {'name': 'Leg Press', 'sets': 3, 'reps': 12, 'weight': 150 + i*10},
            {'name': 'Leg Curls', 'sets': 3, 'reps': 15, 'weight': 40 + i*2},
            {'name': 'Calf Raises', 'sets': 4, 'reps': 20, 'weight': 50 + i*5}
        ]
        
        entry = ProgressEntry(
            workout_name="Leg Day",
            date=date,
            exercises_completed=exercises_done,
            notes=f"Session {i+1} - feeling stronger!"
        )
        
        app.log_progress(entry)
        print(f"✓ Logged session {i+1} with {len(exercises_done)} exercises")
    print()
    
    # Demo 4: View progress history
    print("📊 DEMO 4: Viewing Progress History")
    print("-" * 70)
    
    history = app.get_progress_history(workout_name="Leg Day")
    print(f"Total sessions logged: {len(history)}\n")
    
    for i, entry in enumerate(history[:3], 1):  # Show last 3
        print(f"Session {i}:")
        print(f"  Date: {entry.date[:10]}")
        print(f"  Exercises:")
        for ex in entry.exercises_completed[:2]:  # Show first 2 exercises
            print(f"    - {ex['name']}: {ex['sets']}x{ex['reps']} @ {ex['weight']}kg")
        if entry.notes:
            print(f"  Notes: {entry.notes}")
        print()
    
    # Demo 5: View statistics
    print("📈 DEMO 5: Workout Statistics")
    print("-" * 70)
    
    stats = app.get_workout_stats("Leg Day")
    print(f"Workout: {stats['workout_name']}")
    print(f"Total Sessions: {stats['total_sessions']}")
    print(f"Last Workout: {stats['last_workout'][:10] if stats['last_workout'] else 'N/A'}")
    print()
    
    # Demo 6: Progress progression visualization
    print("💪 DEMO 6: Progress Progression")
    print("-" * 70)
    
    print("Squat weight progression:")
    for i, entry in enumerate(reversed(history), 1):
        squat = next((ex for ex in entry.exercises_completed if ex['name'] == 'Barbell Squat'), None)
        if squat:
            bars = '█' * (squat['weight'] // 10)
            print(f"  Session {i}: {bars} {squat['weight']}kg")
    print()
    
    print("=" * 70)
    print("Demo completed! 🎉")
    print("=" * 70)
    print("\nKey Features Demonstrated:")
    print("✅ Create custom workout plans")
    print("✅ Log workout sessions with detailed exercise data")
    print("✅ Track progress over time")
    print("✅ View workout statistics")
    print("✅ Visualize strength progression")
    print("\nRun 'python gym_app.py' to try the interactive CLI!")

if __name__ == "__main__":
    demo()
