(function () {
  const nativeFetch = window.fetch.bind(window);
  const config = window.APP_CONFIG || {};
  const apiBaseUrl = String(config.api_base_url || "").trim();

  function isApiPath(input) {
    return typeof input === "string" && input.startsWith("/api/");
  }

  function resolveApiInput(input) {
    if (!isApiPath(input) || !apiBaseUrl) {
      return input;
    }
    return `${apiBaseUrl.replace(/\/$/, "")}${input}`;
  }

  async function fetchWithRetry(input, init = {}, retries = 1) {
    const method = String((init && init.method) || "GET").toUpperCase();
    const allowRetry = method === "GET" || method === "HEAD" || method === "OPTIONS";
    let attempt = 0;

    while (true) {
      try {
        const response = await nativeFetch(resolveApiInput(input), init);
        if (!allowRetry || response.ok || response.status < 500 || attempt >= retries) {
          return response;
        }
      } catch (error) {
        if (!allowRetry || attempt >= retries) {
          throw error;
        }
      }
      attempt += 1;
    }
  }

  window.fetch = function (input, init) {
    if (!isApiPath(input)) {
      return nativeFetch(input, init);
    }
    return fetchWithRetry(input, init);
  };

  window.apiFetchJson = async function (input, init) {
    const response = await window.fetch(input, init);
    const text = await response.text();
    let payload = null;

    if (text) {
      try {
        payload = JSON.parse(text);
      } catch (error) {
        payload = text;
      }
    }

    if (!response.ok) {
      const message =
        payload && typeof payload === "object" && payload.detail
          ? payload.detail
          : `Request failed with status ${response.status}.`;
      throw new Error(message);
    }

    return payload;
  };
})();
