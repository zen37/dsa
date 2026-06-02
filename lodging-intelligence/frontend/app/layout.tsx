import "./globals.css";
import Link from "next/link";

export const metadata = {
  title: "Lodging Intelligence",
  description: "Lodging document intelligence MVP"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="shell">
          <header className="topbar">
            <div className="topbar-inner">
              <Link className="brand" href="/">
                Lodging Intelligence
              </Link>
              <nav className="nav">
                <Link href="/upload">Upload</Link>
                <Link href="/documents">Documents</Link>
              </nav>
            </div>
          </header>
          <main className="main">{children}</main>
        </div>
      </body>
    </html>
  );
}
