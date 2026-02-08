# Gym App - Quick Start Guide

## Overview
Ritt is a comprehensive gym tracking application that helps you create workout plans and monitor your fitness progress.

## Installation

```bash
git clone https://github.com/royrituparnaofficial-hub/Ritt.git
cd Ritt
```

No external dependencies required! Uses Python standard library only.

## Quick Start

### 1. Run the Demo
See all features in action:
```bash
python demo.py
```

### 2. Start the Interactive App
```bash
python gym_app.py
```

### 3. Try the Sample Workout
1. Select option 5 to create a sample plan
2. Select option 1 to view the plan details
3. Select option 2 to log a workout
4. Select option 3 to view your progress

## Main Features

### 1️⃣ Create Workout Plans
Design custom workout plans with:
- Multiple workouts per plan
- Specific exercises with sets, reps, and weights
- Day assignments (e.g., Monday/Thursday)
- Descriptive notes

### 2️⃣ Log Progress
Track your workouts by recording:
- Which workout you completed
- Exercises performed
- Sets, reps, and weight used
- Personal notes

### 3️⃣ View History
Review your training history:
- See all logged workouts
- Filter by date range
- Filter by workout name
- Track improvements over time

### 4️⃣ Get Statistics
Analyze your training:
- Total sessions completed
- Last workout date
- Consistency tracking

## Sample Plan Included

The app includes a complete **Push/Pull/Legs Split**:

**Push Day (Monday/Thursday)**
- Bench Press: 4x8 @ 60kg
- Overhead Press: 3x10 @ 40kg
- Incline DB Press: 3x12 @ 20kg
- Tricep Dips: 3x12
- Lateral Raises: 3x15 @ 10kg

**Pull Day (Tuesday/Friday)**
- Deadlift: 4x6 @ 100kg
- Pull-ups: 3x10
- Barbell Rows: 4x8 @ 60kg
- Face Pulls: 3x15 @ 15kg
- Bicep Curls: 3x12 @ 15kg

**Leg Day (Wednesday/Saturday)**
- Squats: 4x8 @ 80kg
- Romanian Deadlift: 3x10 @ 60kg
- Leg Press: 3x12 @ 100kg
- Leg Curls: 3x12 @ 30kg
- Calf Raises: 4x15 @ 40kg

## Data Storage

All data is stored locally in JSON format:
- `data/workout_plans.json` - Your workout plans
- `data/progress.json` - Your progress logs

## Running Tests

Verify everything works:
```bash
python -m unittest test_gym_app.py -v
```

Expected output: 17 tests passing ✅

## Example Usage

### Creating a Custom Plan
```python
from gym_app import Exercise, Workout, WorkoutPlan, GymApp

# Define exercises
exercises = [
    Exercise("Bench Press", sets=4, reps=8, weight=60),
    Exercise("Dumbbell Flyes", sets=3, reps=12, weight=20)
]

# Create workout
workout = Workout("Chest Day", exercises, day="Monday")

# Create plan
plan = WorkoutPlan(
    name="Upper Body Program",
    workouts=[workout],
    description="Focus on chest and arms"
)

# Save it
app = GymApp()
app.create_workout_plan(plan)
```

### Logging a Workout
```python
from gym_app import ProgressEntry, GymApp
from datetime import datetime

# Log what you did
exercises_done = [
    {'name': 'Bench Press', 'sets': 4, 'reps': 8, 'weight': 60},
    {'name': 'Dumbbell Flyes', 'sets': 3, 'reps': 12, 'weight': 20}
]

entry = ProgressEntry(
    workout_name="Chest Day",
    date=datetime.now().isoformat(),
    exercises_completed=exercises_done,
    notes="Great pump today!"
)

app = GymApp()
app.log_progress(entry)
```

## Tips for Success

1. **Start with the sample plan** - Use option 5 to create it
2. **Log consistently** - Record every workout for best tracking
3. **Add notes** - Document how you felt, PRs achieved, etc.
4. **Review progress** - Check your history regularly for motivation
5. **Adjust weights** - Update exercises as you get stronger

## Architecture

```
Exercise ──┐
           ├──> Workout ──┐
Exercise ──┘             ├──> WorkoutPlan ──> GymApp
                         │                       │
ProgressEntry ───────────┘                       ├──> JSON Files
                                                  │
                                                  └──> CLI Interface
```

## Support

For issues or questions:
- Check the README.md for detailed documentation
- Review test_gym_app.py for code examples
- Run demo.py to see features in action

---

**Keep training hard! 💪**
