import React from 'react';

export function ButterflowLogo() {
  return (
    <svg
      width="64"
      height="64"
      viewBox="0 0 360 360"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="w-16 h-16 sm:w-20 sm:h-20"
    >
      <path
        d="M40 180 C40 180, 90 40, 180 180 S320 180, 320 180"
        fill="url(#butterflow-gradient)"
        strokeLinecap="round"
      />
      <defs>
        <linearGradient id="butterflow-gradient" x1="40" y1="180" x2="320" y2="180" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="#3B82F6"/>
          <stop offset="100%" stopColor="#2563EB"/>
        </linearGradient>
      </defs>
    </svg>
  );
}