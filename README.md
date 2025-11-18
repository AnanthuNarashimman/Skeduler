# Intelligent Timetable Scheduler

*Project Status: ⚠️ Under Active Development ⚠️*

## Project Goal

This project aims to replace the complex, time-consuming, and error-prone manual process of creating the departmental timetable. It uses a powerful optimization engine to generate a complete, conflict-free schedule for all classes and staff, respecting all real-world constraints.

## Core Technology

This project is built using Constraint Programming (CP), the industry-standard method for solving large-scale scheduling problems.

Engine: Google OR-Tools (CP-SAT Solver)

Language: Python

Approach: We use a sophisticated two-step optimization process to solve this highly complex problem efficiently:

Staff Assignment Model: First, a model runs to assign the best-qualified staff to each subject, with the primary goal of balancing the total weekly workload as fairly as possible.

Scheduling Model: Second, the optimized staff assignments are fed into the main scheduling model, which solves the "when" puzzle, placing all periods onto the timetable without conflicts.
