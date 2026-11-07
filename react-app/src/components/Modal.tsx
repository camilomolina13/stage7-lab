import type { ReactNode } from "react";

interface Props {
  title: string;
  children: ReactNode;
}

export default function Modal({ title, children }: Props) {
  return (
    <div className="overlay">
      <div className="modal" role="dialog" aria-modal="true" aria-label={title}>
        <h2>{title}</h2>
        {children}
      </div>
    </div>
  );
}