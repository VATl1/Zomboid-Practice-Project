import { useEffect, useState } from "react";

const API = "http://localhost:8000";

function App() {
  const [items, setItems] = useState([]);
  const [stats, setStats] = useState({});
  const [filter, setFilter] = useState("");
  const [form, setForm] = useState({ name: "", type: "", condition: "", amount: "" });
  const [editId, setEditId] = useState(null);

 
  const loadData = async () => {
    const resItems = await fetch(`${API}/items`);
    const dataItems = await resItems.json();
    setItems(dataItems);

    const resStats = await fetch(`${API}/stats/condition`);
    const dataStats = await resStats.json();
    setStats(dataStats);
  };

  useEffect(() => {
    loadData();
  }, []);

 
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.name || !form.type || !form.condition || !form.amount) return;

    const method = editId ? "PUT" : "POST";
    const url = editId ? `${API}/items/${editId}` : `${API}/items`;

    await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: form.name,
        type: form.type,
        condition: form.condition,
        amount: parseInt(form.amount),
      }),
    });

    setForm({ name: "", type: "", condition: "", amount: "" });
    setEditId(null);
    await loadData();
  };


  const handleDelete = async (id) => {
    await fetch(`${API}/items/${id}`, { method: "DELETE" });
    await loadData();
  };


  const startEdit = (item) => {
    setEditId(item.id);
    setForm({
      name: item.name,
      type: item.type,
      condition: item.condition,
      amount: item.amount,
    });
  };


  const filteredItems = items.filter((i) =>
    i.name.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-zinc-950 text-gray-100 flex flex-col items-center p-8">
      <h1 className="text-4xl font-bold mb-6 text-emerald-400">
         Zomboid Accounting System
      </h1>


      <input
        type="text"
        placeholder="🔍 Пошук за назвою..."
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        className="mb-6 w-full max-w-md p-2 rounded bg-zinc-800 border border-zinc-700 focus:ring-2 focus:ring-emerald-400 outline-none"
      />


      <div className="w-full max-w-4xl overflow-x-auto">
        <table className="w-full border-collapse border border-zinc-700 text-sm">
          <thead className="bg-zinc-800 text-emerald-300">
            <tr>
              <th className="border border-zinc-700 px-3 py-2">ID</th>
              <th className="border border-zinc-700 px-3 py-2">Name</th>
              <th className="border border-zinc-700 px-3 py-2">Type</th>
              <th className="border border-zinc-700 px-3 py-2">Condition</th>
              <th className="border border-zinc-700 px-3 py-2">Amount</th>
              <th className="border border-zinc-700 px-3 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredItems.map((item) => (
              <tr
                key={item.id}
                className="hover:bg-zinc-800 transition-colors duration-150"
              >
                <td className="border border-zinc-700 px-3 py-2 text-center">{item.id}</td>
                <td className="border border-zinc-700 px-3 py-2">{item.name}</td>
                <td className="border border-zinc-700 px-3 py-2">{item.type}</td>
                <td className="border border-zinc-700 px-3 py-2">{item.condition}</td>
                <td className="border border-zinc-700 px-3 py-2 text-center">{item.amount}</td>
                <td className="border border-zinc-700 px-3 py-2 text-center space-x-2">
                  <button
                    onClick={() => startEdit(item)}
                    className="px-2 py-1 bg-blue-600 rounded hover:bg-blue-500"
                  >
                    ✍️
                  </button>
                  <button
                    onClick={() => handleDelete(item.id)}
                    className="px-2 py-1 bg-red-600 rounded hover:bg-red-500"
                  >
                    🗑️
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>


      <div className="mt-10 w-full max-w-md bg-zinc-800 rounded-lg p-4 border border-zinc-700">
        <h2 className="text-xl font-semibold mb-3 text-emerald-300">
           Статистика станів
        </h2>
        <ul className="space-y-1">
          {Object.entries(stats).map(([cond, perc]) => (
            <li key={cond} className="flex justify-between">
              <span>{cond}</span>
              <span className="text-emerald-400">{perc}%</span>
            </li>
          ))}
        </ul>
      </div>


      <form
        onSubmit={handleSubmit}
        className="mt-10 flex flex-col gap-3 w-full max-w-3xl bg-zinc-800 p-4 rounded-lg border border-zinc-700"
      >
        <h2 className="text-xl font-semibold text-emerald-300">
          {editId ? "✍️ Редагувати предмет" : "Додати новий предмет"}
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <input
            type="text"
            placeholder="Name"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            className="p-2 rounded bg-zinc-900 border border-zinc-700"
          />
          <input
            type="text"
            placeholder="Type"
            value={form.type}
            onChange={(e) => setForm({ ...form, type: e.target.value })}
            className="p-2 rounded bg-zinc-900 border border-zinc-700"
          />
          <input
            type="text"
            placeholder="Condition"
            value={form.condition}
            onChange={(e) => setForm({ ...form, condition: e.target.value })}
            className="p-2 rounded bg-zinc-900 border border-zinc-700"
          />
          <input
            type="number"
            placeholder="Amount"
            value={form.amount}
            onChange={(e) => setForm({ ...form, amount: e.target.value })}
            className="p-2 rounded bg-zinc-900 border border-zinc-700"
          />
        </div>
        <button
          type="submit"
          className="mt-3 bg-emerald-600 hover:bg-emerald-500 text-white py-2 rounded"
        >
          {editId ? "Зберегти зміни" : "Додати"}
        </button>
      </form>
    </div>
  );
}

export default App;
