# Ritt - Gym Tracker App

A comprehensive gym app that helps you create workout plans and track your progress over time.

## Features

- ✅ **Create Workout Plans**: Design custom workout plans with multiple workouts and exercises
- ✅ **Track Progress**: Log completed workouts with sets, reps, and weights
- ✅ **View History**: Review your workout history and track improvements
- ✅ **Workout Statistics**: Get insights into your training frequency and consistency
- ✅ **Sample Plans**: Quick-start with pre-built workout templates

## Installation

1. Clone the repository:
```bash
git clone https://github.com/royrituparnaofficial-hub/Ritt.git
cd Ritt
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the App

Start the interactive CLI:
```bash
python gym_app.py
```

### Main Menu Options

1. **Create/View Workout Plans** - Browse and view your saved workout plans
2. **Log Workout Progress** - Record completed workout sessions
3. **View Progress History** - See all your logged workouts
4. **View Workout Stats** - Get statistics for specific workouts
5. **Create Sample Plan** - Generate a sample Push/Pull/Legs split plan
6. **Exit** - Close the application

### Example Workflow

1. Create a sample plan (Option 5)
2. View the plan details (Option 1)
3. Complete a workout and log it (Option 2)
4. Check your progress history (Option 3)
5. View statistics for tracked workouts (Option 4)

## Data Storage

All data is stored locally in JSON format in the `data/` directory:
- `workout_plans.json` - Your saved workout plans
- `progress.json` - Your workout progress logs

## Running Tests

Run the test suite:
```bash
python -m unittest test_gym_app.py
```

Or run with verbose output:
```bash
python -m unittest test_gym_app.py -v
```

## Project Structure

```
Ritt/
├── gym_app.py           # Main application code
├── test_gym_app.py      # Test suite
├── requirements.txt     # Python dependencies
├── data/               # Data storage directory
│   ├── workout_plans.json
│   └── progress.json
└── README.md           # This file
```

## Classes and Components

### Core Classes

- **Exercise**: Represents a single exercise with sets, reps, and optional weight
- **Workout**: Collection of exercises for a single workout session
- **WorkoutPlan**: Complete workout plan with multiple workouts
- **ProgressEntry**: Log entry for a completed workout
- **GymApp**: Main application class managing plans and progress

### Key Features

#### Creating Custom Workout Plans

```python
from gym_app import Exercise, Workout, WorkoutPlan, GymApp

# Create exercises
bench = Exercise("Bench Press", sets=4, reps=8, weight=60)
squat = Exercise("Squat", sets=4, reps=10, weight=100)

# Create workout
upper_body = Workout("Upper Body", [bench], day="Monday")

# Create plan
plan = WorkoutPlan("My Plan", [upper_body], "Custom strength plan")

# Save plan
app = GymApp()
app.create_workout_plan(plan)
```

#### Logging Progress

```python
from gym_app import ProgressEntry, GymApp
from datetime import datetime

# Log a workout
exercises_done = [
    {'name': 'Bench Press', 'sets': 4, 'reps': 8, 'weight': 60},
    {'name': 'Squat', 'sets': 4, 'reps': 10, 'weight': 100}
]

entry = ProgressEntry(
    workout_name="Upper Body",
    date=datetime.now().isoformat(),
    exercises_completed=exercises_done,
    notes="Great workout!"
)

app = GymApp()
app.log_progress(entry)
```

## Sample Workout Plan

The app includes a sample "Push/Pull/Legs Split" plan with:

- **Push Day** (Monday/Thursday): Bench press, overhead press, dumbbell press, triceps, shoulders
- **Pull Day** (Tuesday/Friday): Deadlifts, pull-ups, rows, face pulls, biceps
- **Leg Day** (Wednesday/Saturday): Squats, RDLs, leg press, leg curls, calves

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

MIT License - feel free to use this app for your fitness journey! 💪
