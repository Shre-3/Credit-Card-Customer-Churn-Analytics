const pages = [
  { key: "eda", label: "EDA" },
  { key: "model", label: "Model" },
  { key: "customer", label: "Customer" },
  { key: "prediction", label: "Prediction" },
  { key: "business", label: "Business Impact" },
];

export function Layout({ activePage, onPageChange, children }) {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-950">
      <aside className="fixed inset-y-0 left-0 hidden w-72 border-r border-slate-200 bg-slate-950 p-6 text-white lg:block">
        <p className="text-xs font-semibold uppercase tracking-[0.35em] text-cyan-300">Bank Analytics</p>
        <h1 className="mt-4 text-2xl font-bold leading-tight">Credit Card Customer Churn Analytics Platform</h1>
        <p className="mt-4 text-sm text-slate-300">
          Identify churn risk, explain customer behavior, and quantify retention upside.
        </p>
        <nav className="mt-10 space-y-2">
          {pages.map((page) => (
            <button
              className={`w-full rounded-xl px-4 py-3 text-left text-sm font-medium transition ${
                activePage === page.key ? "bg-cyan-400 text-slate-950" : "text-slate-300 hover:bg-slate-800"
              }`}
              key={page.key}
              onClick={() => onPageChange(page.key)}
              type="button"
            >
              {page.label}
            </button>
          ))}
        </nav>
      </aside>

      <div className="lg:pl-72">
        <header className="sticky top-0 z-10 border-b border-slate-200 bg-white/90 px-4 py-4 backdrop-blur lg:hidden">
          <select
            className="w-full rounded-xl border border-slate-300 bg-white px-3 py-2"
            onChange={(event) => onPageChange(event.target.value)}
            value={activePage}
          >
            {pages.map((page) => (
              <option key={page.key} value={page.key}>
                {page.label}
              </option>
            ))}
          </select>
        </header>
        <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">{children}</main>
      </div>
    </div>
  );
}
