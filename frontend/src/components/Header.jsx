import React from 'react';

export default function Header({ status, statusColor }) {
  return (
    <header className="border-b-2 border-abyss-accent mb-5 pb-3 flex justify-between items-center">
      <h1 className="text-abyss-accent text-2xl font-bold tracking-wider">👹 ABYSSUS COMPILER 2.0</h1>
      <span>Status: <strong style={{ color: statusColor }}>{status}</strong></span>
    </header>
  );
}