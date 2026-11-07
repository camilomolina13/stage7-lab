import { useState } from "react";
import { describeError } from "../api/client";
import type { Task } from "../types";
import ErrorBanner from "./ErrorBanner";

interface Props {
  task: Task;
  onConfirm: () => Promise<void>;
  onCancel: () => void;
}

export default function ConfirmDelete({ task, onConfirm, onCancel }: Props) {
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState("");

  async function handleDelete() {
    setDeleting(true);
    setError("");
    try {
      await onConfirm();
    } catch (err) {
      setError(describeError(err).message);
      setDeleting(false);
    }
  }

  return (
    <>
      <ErrorBanner message={error} />
      <p>Are you sure you want to delete:</p>
      <p><strong>"{task.title}"</strong>?</p>
      <p>This action cannot be undone.</p>
      <div className="actions">
        <button className="btn" onClick={onCancel} disabled={deleting}>Cancel</button>
        <button className="btn danger" onClick={handleDelete} disabled={deleting}>
          {deleting ? "Deleting..." : "Delete"}
        </button>
      </div>
    </>
  );
}