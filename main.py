from fastapi import FastAPI, HTTPException

app = FastAPI()

# "מסד נתונים" בזיכרון
tasks = []
counter = 1

@app.get("/tasks")
def get_tasks(priority : int = None):
    if priority == None:
         return tasks
    if priority not in [1,2,3] :
         raise HTTPException(status_code= 400, detail= "Can filter only prio of 1 / 2 / 3 ")
    prior_tasks = []
    for task in tasks:
        if task.get("priority") == priority:
            prior_tasks.append(task)
    return prior_tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks")
def add_task(task: dict):
    global counter
    priority = task.get("priority")
    # Default is 2 if no value is given
    if priority is None :
         priority = 2         
    if priority not in [1,2,3]:
                raise HTTPException(status_code=400, detail= "Priority should be 1 OR 2 OR 3 only")
    new_task = {
        "id": counter,
        "title": task.get("title"),
        "owner": task.get("owner"),
        "priority" : priority
    }
    tasks.append(new_task)
    counter += 1
    return new_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
