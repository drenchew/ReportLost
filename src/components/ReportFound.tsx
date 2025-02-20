import React, { useEffect, useState } from "react";
import axios from "axios";

interface FoundItem {
  _id: string;  // MongoDB stores _id, not id
  title: string;
  description: string;
  imageUrl?: string;  // Image URL (optional)
}

export const ReportFound: React.FC = () => {
  const [foundItems, setFoundItems] = useState<FoundItem[]>([]);

  useEffect(() => {
    const fetchFoundItems = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:5000/api/report-found");
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
            <div key={item._id} className="p-4 border border-gray-300 rounded">
              {item.imageUrl && (
                <img
                  src={item.imageUrl}
                  alt={item.title}
                  className="max-w-full max-h-96 mx-auto rounded"
                />
              )}
              <h3 className="text-lg font-semibold mt-2">{item.title}</h3>
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

export default ReportFound;
