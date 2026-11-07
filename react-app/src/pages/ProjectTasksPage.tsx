import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { describeError } from "../api/client";
import { getProject } from "../api/projects";
import { createTask, deleteTask, getTasks, updateTask } from "../api/tasks";
import ConfirmDelete from "../components/ConfirmDelete";
import ErrorBanner from "../components/ErrorBanner";
import Modal from "../components/Modal";
import TaskForm from "../components/TaskForm";
import type { TaskFormValues } from "../components/TaskForm";
import { PRIORITIES, STATUSES } from "../types";
import type { Priority, Project, Status, Task } from "../types";

// "2026-11-15" -> "Nov 15, 2026" (sin pasar por Date(string) para evitar desfase de zona horaria)
function formatDate(value: string | null) {
  if (!value) return "No due date";
  const [y, m, d] = value.split("-").map(Number);
  return new Date(y, m - 1, d).toLocaleDateString("en-US", {
    month: "short", day: "numeric", year: "numeric",
  });
}

export default function ProjectTasksPage() {
  const { projectId } = useParams();
  const id = Number(projectId);

  const [project, setProject] = useState<Project | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");

  const [statusFilter, setStatusFilter] = useState<Status | "ALL">("ALL");
  const [priorityFilter, setPriorityFilter] = useState<Priority | "ALL">("ALL");

  const [formTask, setFormTask] = useState<Task | "new" | null>(null);
  const [deletingTask, setDeletingTask] = useState<Task | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const [proj, list] = await Promise.all([getProject(id), getTasks(id)]);
        setProject(proj);
        setTasks(list);
      } catch (err) {
        setLoadError(describeError(err).message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [id]);

  // USER-07: filtrado en el frontend
  const visibleTasks = useMemo(
    () =>
      tasks.filter(
        (t) =>
          (statusFilter === "ALL" || t.status === statusFilter) &&
          (priorityFilter === "ALL" || t.priority === priorityFilter),
      ),
    [tasks, statusFilter, priorityFilter],
  );

  async function handleSubmit(values: TaskFormValues) {
    if (formTask === "new") {
      const created = await createTask({ ...values, project_id: id }); // proyecto seleccionado
      setTasks((prev) => [...prev, created]);
    } else if (formTask) {
      const updated = await updateTask(formTask.id, { ...values, project_id: formTask.project_id });
      setTasks((prev) => prev.map((t) => (t.id === updated.id ? updated : t)));
    }
    setFormTask(null);
  }

  async function handleDelete() {
    if (!deletingTask) return;
    await deleteTask(deletingTask.id); // si falla, lanza error y NO se toca la lista
    setTasks((prev) => prev.filter((t) => t.id !== deletingTask.id));
    setDeletingTask(null);
  }

  if (loading) return <p>Loading...</p>;
  if (loadError || !project) {
    return (
      <section>
        <Link to="/">&larr; Projects</Link>
        <ErrorBanner message={loadError || "Project not found."} />
      </section>
    );
  }

  return (
    <section>
      <Link to="/">&larr; Projects</Link>
      <div className="page-header">
        <div>
          <h1>{project.name}</h1>
          <p className="muted">{project.description}</p>
        </div>
        <button className="btn primary" onClick={() => setFormTask("new")}>+ New Task</button>
      </div>

      <div className="filters">
        <label>
          Status:{" "}
          <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value as Status | "ALL")}>
            <option value="ALL">All</option>
            {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
          </select>
        </label>
        <label>
          Priority:{" "}
          <select value={priorityFilter} onChange={(e) => setPriorityFilter(e.target.value as Priority | "ALL")}>
            <option value="ALL">All</option>
            {PRIORITIES.map((p) => <option key={p} value={p}>{p}</option>)}
          </select>
        </label>
      </div>

      {tasks.length === 0 && <p className="muted">This project has no tasks yet.</p>}
      {tasks.length > 0 && visibleTasks.length === 0 && (
        <p className="muted">No tasks match the selected filters.</p>
      )}

      {visibleTasks.map((task) => (
        <article key={task.id} className="card">
          <div>
            <h3>
              {task.title} <span className={`badge ${task.priority}`}>{task.priority}</span>
            </h3>
            <p className="muted">{task.description}</p>
            <p>Status: <strong>{task.status}</strong> &nbsp; Due: {formatDate(task.due_date)}</p>
          </div>
          <div className="actions">
            <button className="btn" onClick={() => setFormTask(task)}>Edit</button>
            <button className="btn danger" onClick={() => setDeletingTask(task)}>Delete</button>
          </div>
        </article>
      ))}

      {formTask && (
        <Modal title={formTask === "new" ? "New Task" : "Edit Task"}>
          <TaskForm
            initial={formTask === "new" ? undefined : formTask}
            onSubmit={handleSubmit}
            onCancel={() => setFormTask(null)}
          />
        </Modal>
      )}

      {deletingTask && (
        <Modal title="Delete Task">
          <ConfirmDelete task={deletingTask} onConfirm={handleDelete} onCancel={() => setDeletingTask(null)} />
        </Modal>
      )}
    </section>
  );
}