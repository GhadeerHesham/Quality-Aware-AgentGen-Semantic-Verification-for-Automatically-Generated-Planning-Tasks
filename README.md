# Quality-Aware-AgentGen-Semantic-Verification-for-Automatically-Generated-Planning-Tasks
# a simple website to demonstrate AgentGen with added quality verifier

# to run this project:
# Run this in PowerShell:
# cd "C:\Users\balla\Downloads\3alemni website\Quality-Aware-AgentGen-Semantic-Verification-for-Automatically-Generated-Planning-Tasks"
# venv\Scripts\python.exe app.py

# Then open: http://127.0.0.1:5000/

# If you want to rebuild the data/model results first:

# venv\Scripts\python.exe generate_benchmark_tasks.py
# venv\Scripts\python.exe agentgen_pipeline.py
# venv\Scripts\python.exe distillation\build_verified_dataset.py
# venv\Scripts\python.exe distillation\train_student.py
# venv\Scripts\python.exe distillation\evaluate_student.py
# venv\Scripts\python.exe evaluate_thesis_comparison.py
# venv\Scripts\python.exe app.py

# GitHub Repo: https://github.com/GhadeerHesham/Quality-Aware-AgentGen-Semantic-Verification-for-Automatically-Generated-Planning-Tasks