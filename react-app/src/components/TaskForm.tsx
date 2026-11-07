import { useState } from "react";
import type { FormEvent } from "react";
import { describeError } from "../api/client";
import { PRIORITIES, STATUSES } from "../types";
import type { FieldErrors, Priority, Status, Task, TaskInput } from "../types";
import ErrorBanner from "./ErrorBanner";

export type TaskFormValues = Omit<TaskInput, "project_id">;

interface Props {
  initial?: Task;
  onSubmit: (data: TaskFormValues) => Promise<void>;
  onCancel: () => void;
}

export default function TaskForm({ initial, onSubmit, onCancel }: Props) {
  const [title, setTitle] = useState(initial?.title ?? "");
  const [description, setDescription] = useState(initial?.description ?? "");
  const [status, setStatus] = useState<Status>(initial?.status ?? "TODO");
  const [priority, setPriority] = useState<Priority>(initial?.priority ?? "MEDIUM");
  const [dueDate, setDueDate] = useState(initial?.due_date ?? "");
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
  const [formError, setFormError] = useState("");
  const [saving, setSaving] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();

    if (!title.trim()) {
      setFieldErrors({ title: ["Title is required."] });
      setFormError("");
      return;
    }

    setSaving(true);
    setFieldErrors({});
    setFormError("");
    try {
      await onSubmit({
        title: title.trim(),
        description,
        status,
        priority,
        due_date: dueDate || null, // fecha vacía -> null
      });
    } catch (err) {
      const { message, fields } = describeError(err);
      setFormError(message);
      setFieldErrors(fields);
      setSaving(false);
    }
  }

  const errorsFor = (field: string) =>
    fieldErrors[field]?.map((m) => <p key={m} className="field-error">{m}</p>);

  return (
    <form onSubmit={handleSubmit} noValidate>
      <ErrorBanner message={formError} />

      <label htmlFor="title">Title</label>
      <input id="title" value={title} onChange={(e) => setTitle(e.target.value)} />
      {errorsFor("title")}

      <label htmlFor="description">Description</label>
      <textarea id="description" rows={3} value={description} onChange={(e) => setDescription(e.target.value)} />
      {errorsFor("description")}

      <label htmlFor="status">Status</label>
      <select id="status" value={status} onChange={(e) => setStatus(e.target.value as Status)}>
        {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
      </select>
      {errorsFor("status")}

      <label htmlFor="priority">Priority</label>
      <select id="priority" value={priority} onChange={(e) => setPriority(e.target.value as Priority)}>
        {PRIORITIES.map((p) => <option key={p} value={p}>{p}</option>)}
      </select>
      {errorsFor("priority")}

      <label htmlFor="due">Due Date</label>
      <input id="due" type="date" value={dueDate} onChange={(e) => setDueDate(e.target.value)} />
      {errorsFor("due_date")}
      {errorsFor("project_id")}

      <div className="actions">
        <button type="button" className="btn" onClick={onCancel} disabled={saving}>Cancel</button>
        <button type="submit" className="btn primary" disabled={saving}>
          {saving ? "Saving..." : initial ? "Save" : "Create"}
        </button>
      </div>
    </form>
  );
}