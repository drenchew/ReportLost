import React, { useEffect, useState } from "react";
import axios from "axios";

interface FoundItem {
  _id: string;
  title: string;
  description: string;
  imageUrl?: string;
  username: string;
}

export const ReportFound: React.FC = () => {
  const [foundItems, setFoundItems] = useState<FoundItem[]>([]);
  const [currentUser, setCurrentUser] = useState<string | null>(null);

  useEffect(() => {
    // Fetch logged-in user
    const fetchCurrentUser = async () => {
      try {
        const res = await axios.get("/api/session", {
          baseURL: "http://127.0.0.1:5000", 
          withCredentials: true, 
        });
        setCurrentUser(res.data["username"]);
      } catch (error) {
        console.error("Error fetching user session", error);
        setCurrentUser(null);
      }
    };


    const fetchFoundItems = async () => {
      try {
        const res = await axios.get("/api/report-found", {
          baseURL: "http://127.0.0.1:5000", 
        });
        setFoundItems(res.data);
      } catch (error) {
        console.error("Error fetching found items", error);
      }
    };

    fetchCurrentUser();
    fetchFoundItems();
  }, []);

  const handleDelete = async (itemId: string) => {
    if (!currentUser) return;

    try {
      await axios.delete(`/api/delete/${itemId}`, {
        baseURL: "http://127.0.0.1:5000", 
        withCredentials: true, 
      });

      setFoundItems(foundItems.filter((item) => item._id !== itemId));
    } catch (error) {
      console.error("Error deleting found item", error);
    }
  };

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
              {(currentUser === item.username || currentUser === "admin") && (
                <button
                  onClick={() => handleDelete(item._id)}
                  className="bg-red-500 text-white p-2 mt-2 rounded"
                >
                  Delete
                </button>
              )}
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
