// api.js - shared helpers used by every page.
// Loaded with a plain <script> tag, so everything here becomes a global function.

const TOKEN_KEY = "access_token";
const LOGIN_PAGE = "/app/";
const HOME_PAGE = "/app/home.html";

// ---------- Token storage (localStorage survives page reloads and browser restarts) ----------

function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

function removeToken() {
  localStorage.removeItem(TOKEN_KEY);
}

// ---------- Page guards ----------

// For pages that need a logged-in user (home.html).
function requireLogin() {
  if (!getToken()) location.replace(LOGIN_PAGE);
}

// For login/signup pages: if you're already logged in, skip straight to home.
function redirectIfLoggedIn() {
  if (getToken()) location.replace(HOME_PAGE);
}

function logout() {
  removeToken();
  location.replace(LOGIN_PAGE);
}

// ---------- Errors ----------

// FastAPI sends errors as {"detail": ...}.
//  - HTTPException  -> detail is a string, e.g. "Assignment not found"
//  - Validation 422 -> detail is a list, e.g. [{"loc": ["body", "title"], "msg": "..."}]
function formatError(detail, status) {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((err) => {
        const field = (err.loc || []).filter((part) => part !== "body").join(".");
        return field ? `${field}: ${err.msg}` : err.msg;
      })
      .join("\n");
  }
  return `Something went wrong (HTTP ${status}).`;
}

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

// ---------- The fetch wrapper ----------

// Usage:
//   await api("/assignments")                                   -> GET
//   await api("/assignments", { method: "POST", json: {...} })  -> JSON body
//   await api("/auth/login",  { method: "POST", form: {...} })  -> form body
// Returns the parsed JSON (or null for 204 No Content). Throws ApiError on failure.
async function api(path, { method = "GET", json, form } = {}) {
  const headers = {};
  let body;

  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  if (json !== undefined) {
    headers["Content-Type"] = "application/json";
    body = JSON.stringify(json);
  } else if (form !== undefined) {
    // URLSearchParams makes fetch send application/x-www-form-urlencoded
    body = new URLSearchParams(form);
  }

  let response;
  try {
    response = await fetch(path, { method, headers, body });
  } catch {
    throw new ApiError("Could not reach the server. Is it running?", 0);
  }

  // We sent a token but the server rejected it (expired or invalid): start over at login.
  if (response.status === 401 && token) {
    logout();
    throw new ApiError("Your session has expired. Please log in again.", 401);
  }

  if (response.status === 204) return null;

  const data = await response.json().catch(() => null);
  if (!response.ok) {
    throw new ApiError(formatError(data && data.detail, response.status), response.status);
  }
  return data;
}

// Log in and remember the token. Used by both the login and signup pages.
async function login(email, password) {
  // OAuth2 login expects FORM fields named "username" and "password".
  const data = await api("/auth/login", {
    method: "POST",
    form: { username: email, password },
  });
  setToken(data.access_token);
}

// Show a message in an element (textContent, so it's never interpreted as HTML).
function showMessage(element, text, type = "error") {
  element.textContent = text;
  element.className = `message ${type}`;
  element.hidden = !text;
}
