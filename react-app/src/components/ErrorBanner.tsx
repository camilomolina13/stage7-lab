export default function ErrorBanner({ message }: { message: string }) {
  if (!message) return null;
  return (
    <div className="banner-error" role="alert">
      ! {message}
    </div>
  );
}