import React, { useState } from "react";
import axios from "axios";

export const ReportLost: React.FC = () => {
  const [formData, setFormData] = useState({ item: "", description: "" });
  const [response, setResponse] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://127.0.0.1:5000/api/report-lost", formData);
      setResponse(res.data.message);
    } catch (error) {
      console.error("Error submitting form", error);
    }
  };

  return (
    <div className="p-6 max-w-lg mx-auto">
      <h2 className="text-2xl font-bold mb-4">Report Lost Item</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          name="item"
          placeholder="Item Name"
          value={formData.item}
          onChange={handleChange}
          className="w-full p-2 border border-gray-300 rounded"
          required
        />
        <textarea
          name="description"
          placeholder="Item Description"
          value={formData.description}
          onChange={handleChange}
          className="w-full p-2 border border-gray-300 rounded"
          required
        />
        <button type="submit" className="w-full p-2 bg-green-500 text-white rounded">
          Submit
        </button>
        
      </form>
      {response && <p className="mt-4 text-green-500">{response}</p>}
    </div>
  );
};
