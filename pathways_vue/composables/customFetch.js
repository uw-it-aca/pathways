import { useTokenStore } from "@/stores/token";

export async function useCustomFetch(url, options = {}) {
  const tokenStore = useTokenStore();

  // Set default headers
  const defaultHeaders = {
    "Access-Control-Allow-Origin": "*",
    "X-CSRFToken": tokenStore.csrfToken,
    "X-Requested-With": "XMLHttpRequest",
  };

  // Merge default headers with any provided in options
  options.headers = {
    ...defaultHeaders,
    ...options.headers,
  };

  try {
    const response = await fetch(url, options);

    // Handle expired session (403 status)
    if (response.status === 403) {
      throw new Error("SessionExpired");
      return;
    }

    // Check if response is ok (status 2xx)
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    // Parse and return JSON response
    return response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
}
