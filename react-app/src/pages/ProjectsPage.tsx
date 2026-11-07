import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { describeError } from "../api/client";
import { createProject, getProjects, updateProject } from "../api/projects";
import ErrorBanner from "../components/ErrorBanner";
import Modal from "../components/Modal";
import ProjectForm from "../components/ProjectForm";
import type { Project, ProjectInput } from "../types";

export default function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  // "new" = crear, un Project = editar, null = modal cerrado
  const [editing, setEditing] = useState<Project | "new" | null>(null);

  useEffect(() => {
    async function load() {
      try {
        setProjects(await getProjects());
      } catch (err) {
        setLoadError(describeError(err).message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  async function handleSubmit(data: ProjectInput) {
    if (editing === "new") {
      const created = await createProject(data);
      setProjects((prev) => [...prev, created]); // aparece sin recargar
    } else if (editing) {
      const updated = await updateProject(editing.id, data);
      setProjects((prev) => prev.map((p) => (p.id === updated.id ? updated : p)));
    }
    setEditing(null); // solo se cierra si la API respondió bien
  }

  return (
    <section>
      <div className="page-header">
        <h1>Projects</h1>
        <button className="btn primary" onClick={() => setEditing("new")}>+ New Project</button>
      </div>

      <ErrorBanner message={loadError} />
      {loading && <p>Loading projects...</p>}
      {!loading && !loadError && projects.length === 0 && (
        <p className="muted">No projects yet. Create the first one.</p>
      )}

      {projects.map((project) => (
        <article key={project.id} className="card">
          <div>
            <h3>{project.name}</h3>
            <p className="muted">{project.description}</p>
          </div>
          <div className="actions">
            <Link className="btn" to={`/projects/${project.id}`}>Open</Link>
            <button className="btn" onClick={() => setEditing(project)}>Edit</button>
          </div>
        </article>
      ))}

      {editing && (
        <Modal title={editing === "new" ? "Create Project" : "Edit Project"}>
          <ProjectForm
            initial={editing === "new" ? undefined : editing}
            onSubmit={handleSubmit}
            onCancel={() => setEditing(null)}
          />
        </Modal>
      )}
    </section>
  );
}