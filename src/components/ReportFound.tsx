import React, { useEffect, useState } from "react";
import axios from "axios";

interface FoundItem {
  id: number;
  item: string;
  description: string;
  imageUrl: string;
}

export const ReportFound: React.FC = () => {
  const [foundItems, setFoundItems] = useState<FoundItem[]>([]);

  useEffect(() => {
    const fetchFoundItems = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:5000/api/found-items");
        setFoundItems(res.data);
      } catch (error) {
        console.error("Error fetching found items", error);
      }
    };

    fetchFoundItems();
  }, []);

  return (
    <div className="p-6 max-w-lg mx-auto">
      <h2 className="text-2xl font-bold mb-4">Found Items</h2>
      <div className="space-y-4 max-h-96 overflow-y-auto border p-4 rounded">
        {foundItems.length > 0 ? (
          foundItems.map((item) => (
            <div key={item.id} className="p-4 border border-gray-300 rounded">
              <img src={item.imageUrl} alt={item.item} className="w-full h-48 object-cover rounded" />
              <h3 className="text-lg font-semibold mt-2">{item.item}</h3>
              <p className="text-gray-600">{item.description}</p>
            </div>
          ))
        ) : (
          <p className="text-gray-500">No found items reported yet.</p>
        )}
      </div>
    </div>
  );
};
