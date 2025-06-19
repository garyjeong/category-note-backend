import "@testing-library/jest-dom";

// Mock environment variables
globalThis.process = globalThis.process || { env: {} };
globalThis.process.env = globalThis.process.env || {};
globalThis.process.env.NEXT_PUBLIC_API_URL = "http://localhost:8000";
