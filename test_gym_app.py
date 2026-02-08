#!/usr/bin/env python3
"""
Tests for Gym App
"""

import unittest
import os
import json
import tempfile
import shutil
from datetime import datetime
from gym_app import (
    Exercise, Workout, WorkoutPlan, ProgressEntry, GymApp, create_sample_plan
)


class TestExercise(unittest.TestCase):
    """Test Exercise class"""
    
    def test_create_exercise(self):
        ex = Exercise("Bench Press", 3, 10, 60)
        self.assertEqual(ex.name, "Bench Press")
        self.assertEqual(ex.sets, 3)
        self.assertEqual(ex.reps, 10)
        self.assertEqual(ex.weight, 60)
    
    def test_exercise_to_dict(self):
        ex = Exercise("Squat", 4, 8, 100)
        data = ex.to_dict()
        self.assertEqual(data['name'], "Squat")
        self.assertEqual(data['sets'], 4)
        self.assertEqual(data['reps'], 8)
        self.assertEqual(data['weight'], 100)
    
    def test_exercise_from_dict(self):
        data = {'name': 'Deadlift', 'sets': 5, 'reps': 5, 'weight': 120}
        ex = Exercise.from_dict(data)
        self.assertEqual(ex.name, 'Deadlift')
        self.assertEqual(ex.sets, 5)
        self.assertEqual(ex.reps, 5)
        self.assertEqual(ex.weight, 120)


class TestWorkout(unittest.TestCase):
    """Test Workout class"""
    
    def test_create_workout(self):
        exercises = [
            Exercise("Bench Press", 3, 10, 60),
            Exercise("Squat", 4, 8, 100)
        ]
        workout = Workout("Upper Body", exercises, "Monday")
        self.assertEqual(workout.name, "Upper Body")
        self.assertEqual(len(workout.exercises), 2)
        self.assertEqual(workout.day, "Monday")
    
    def test_workout_to_dict(self):
        exercises = [Exercise("Push-up", 3, 15)]
        workout = Workout("Home Workout", exercises)
        data = workout.to_dict()
        self.assertEqual(data['name'], "Home Workout")
        self.assertEqual(len(data['exercises']), 1)
    
    def test_workout_from_dict(self):
        data = {
            'name': 'Leg Day',
            'exercises': [
                {'name': 'Squat', 'sets': 4, 'reps': 8, 'weight': 100}
            ],
            'day': 'Wednesday'
        }
        workout = Workout.from_dict(data)
        self.assertEqual(workout.name, 'Leg Day')
        self.assertEqual(len(workout.exercises), 1)


class TestWorkoutPlan(unittest.TestCase):
    """Test WorkoutPlan class"""
    
    def test_create_plan(self):
        exercises = [Exercise("Bench Press", 3, 10, 60)]
        workout = Workout("Upper", exercises)
        plan = WorkoutPlan("My Plan", [workout], "Test plan")
        self.assertEqual(plan.name, "My Plan")
        self.assertEqual(len(plan.workouts), 1)
        self.assertEqual(plan.description, "Test plan")
    
    def test_plan_to_dict(self):
        exercises = [Exercise("Squat", 4, 8, 100)]
        workout = Workout("Leg Day", exercises)
        plan = WorkoutPlan("Leg Plan", [workout])
        data = plan.to_dict()
        self.assertEqual(data['name'], "Leg Plan")
        self.assertEqual(len(data['workouts']), 1)


class TestProgressEntry(unittest.TestCase):
    """Test ProgressEntry class"""
    
    def test_create_progress_entry(self):
        exercises = [{'name': 'Bench Press', 'sets': 3, 'reps': 10, 'weight': 60}]
        entry = ProgressEntry("Upper Body", datetime.now().isoformat(), exercises, "Felt good")
        self.assertEqual(entry.workout_name, "Upper Body")
        self.assertEqual(len(entry.exercises_completed), 1)
        self.assertEqual(entry.notes, "Felt good")
    
    def test_progress_to_dict(self):
        exercises = [{'name': 'Squat', 'sets': 4, 'reps': 8}]
        entry = ProgressEntry("Leg Day", "2024-01-01", exercises)
        data = entry.to_dict()
        self.assertEqual(data['workout_name'], "Leg Day")
        self.assertEqual(data['date'], "2024-01-01")


class TestGymApp(unittest.TestCase):
    """Test GymApp class"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.app = GymApp(data_dir=self.test_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def test_create_workout_plan(self):
        """Test creating a workout plan"""
        exercises = [Exercise("Bench Press", 3, 10, 60)]
        workout = Workout("Upper", exercises)
        plan = WorkoutPlan("Test Plan", [workout])
        
        result = self.app.create_workout_plan(plan)
        self.assertTrue(result)
        
        # Verify plan was saved
        retrieved_plan = self.app.get_workout_plan("Test Plan")
        self.assertIsNotNone(retrieved_plan)
        self.assertEqual(retrieved_plan.name, "Test Plan")
    
    def test_list_workout_plans(self):
        """Test listing workout plans"""
        # Initially empty
        plans = self.app.list_workout_plans()
        self.assertEqual(len(plans), 0)
        
        # Add a plan
        exercises = [Exercise("Squat", 4, 8)]
        workout = Workout("Leg Day", exercises)
        plan = WorkoutPlan("Plan 1", [workout])
        self.app.create_workout_plan(plan)
        
        # Should have one plan
        plans = self.app.list_workout_plans()
        self.assertEqual(len(plans), 1)
        self.assertIn("Plan 1", plans)
    
    def test_delete_workout_plan(self):
        """Test deleting a workout plan"""
        exercises = [Exercise("Push-up", 3, 15)]
        workout = Workout("Home", exercises)
        plan = WorkoutPlan("Home Plan", [workout])
        
        self.app.create_workout_plan(plan)
        self.assertEqual(len(self.app.list_workout_plans()), 1)
        
        result = self.app.delete_workout_plan("Home Plan")
        self.assertTrue(result)
        self.assertEqual(len(self.app.list_workout_plans()), 0)
    
    def test_log_progress(self):
        """Test logging progress"""
        exercises = [{'name': 'Bench Press', 'sets': 3, 'reps': 10, 'weight': 60}]
        entry = ProgressEntry("Upper Body", datetime.now().isoformat(), exercises)
        
        result = self.app.log_progress(entry)
        self.assertTrue(result)
        
        # Verify progress was saved
        history = self.app.get_progress_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].workout_name, "Upper Body")
    
    def test_get_progress_history_filtered(self):
        """Test getting filtered progress history"""
        # Add multiple entries
        for i in range(3):
            exercises = [{'name': f'Exercise {i}', 'sets': 3, 'reps': 10}]
            entry = ProgressEntry(f"Workout {i % 2}", datetime.now().isoformat(), exercises)
            self.app.log_progress(entry)
        
        # Get all entries
        all_history = self.app.get_progress_history()
        self.assertEqual(len(all_history), 3)
        
        # Filter by workout name
        filtered = self.app.get_progress_history(workout_name="Workout 0")
        self.assertEqual(len(filtered), 2)
    
    def test_get_workout_stats(self):
        """Test getting workout statistics"""
        exercises = [{'name': 'Bench Press', 'sets': 3, 'reps': 10}]
        
        # Log two sessions
        for _ in range(2):
            entry = ProgressEntry("Upper Body", datetime.now().isoformat(), exercises)
            self.app.log_progress(entry)
        
        stats = self.app.get_workout_stats("Upper Body")
        self.assertEqual(stats['total_sessions'], 2)
        self.assertIsNotNone(stats['last_workout'])
        self.assertEqual(stats['workout_name'], "Upper Body")


class TestSamplePlan(unittest.TestCase):
    """Test sample plan creation"""
    
    def test_create_sample_plan(self):
        """Test creating sample plan"""
        plan = create_sample_plan()
        self.assertEqual(plan.name, "Push/Pull/Legs Split")
        self.assertEqual(len(plan.workouts), 3)
        self.assertGreater(len(plan.description), 0)


if __name__ == '__main__':
    unittest.main()
