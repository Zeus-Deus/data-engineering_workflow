// Environment variables helper
export const getEnvironmentVariable = (key: string): string => {
  const value = process.env[key];
  if (!value) {
    throw new Error(`Environment variable ${key} is not defined`);
  }
  return value;
};

// FastAPI URL
export const FASTAPI_URL = getEnvironmentVariable('NEXT_PUBLIC_FASTAPI_URL'); 