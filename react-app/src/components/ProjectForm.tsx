import { useState } from "react";
import type { FormEvent } from "react";
import { describeError } from "../api/client";
import type { FieldErrors, Project, ProjectInput } from "../types";
import ErrorBanner from "./ErrorBanner";

interface Props {
  initial?: Project;
  onSubmit: (data: ProjectInput) => Promise<void>;
  onCancel: () => void;
}

export default function ProjectForm({ initial, onSubmit, onCancel }: Props) {
  const [name, setName] = useState(initial?.name ?? "");
  const [description, setDescription] = useState(initial?.description ?? "");
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
  const [formError, setFormError] = useState("");
  const [saving, setSaving] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();

    // Validación en el cliente: no se envía un formulario inválido
    if (!name.trim()) {
      setFieldErrors({ name: ["Name is required."] });
      setFormError("");
      return;
    }

    setSaving(true);
    setFieldErrors({});
    setFormError("");
    try {
      await onSubmit({ name: name.trim(), description });
    } catch (err) {
      const { message, fields } = describeError(err);
      setFormError(message);
      setFieldErrors(fields);
      setSaving(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} noValidate>
      <ErrorBanner message={formError} />

      <label htmlFor="name">Name</label>
      <input id="name" value={name} onChange={(e) => setName(e.target.value)} />
      {fieldErrors.name?.map((m) => <p key={m} className="field-error">{m}</p>)}

      <label htmlFor="description">Description</label>
      <textarea id="description" rows={3} value={description} onChange={(e) => setDescription(e.target.value)} />
      {fieldErrors.description?.map((m) => <p key={m} className="field-error">{m}</p>)}

      <div className="actions">
        <button type="button" className="btn" onClick={onCancel} disabled={saving}>Cancel</button>
        <button type="submit" className="btn primary" disabled={saving}>
          {saving ? "Saving..." : initial ? "Save" : "Create Project"}
        </button>
      </div>
    </form>
  );
}