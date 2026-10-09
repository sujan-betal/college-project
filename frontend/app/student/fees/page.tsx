"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function StudentFees() {
  const [feeStructure, setFeeStructure] = useState<any[]>([]);
  const [payments, setPayments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.studentFees().then((res) => {
      if (res.success) {
        setFeeStructure(res.data?.fee_structure || []);
        setPayments(res.data?.payments || []);
      }
      setLoading(false);
    });
  }, []);

  function renderTable(rows: any[], label: string, amountLabel: string) {
    return (
      <div className="mt-6 overflow-x-auto rounded-2xl border border-ink/10 bg-white shadow-sm">
        <table className="w-full min-w-[560px] text-sm">
          <thead>
            <tr className="bg-maroon text-cream">
              <th className="px-4 py-3 text-left font-semibold">Head</th>
              <th className="px-4 py-3 text-left font-semibold">{amountLabel}</th>
              <th className="px-4 py-3 text-left font-semibold">Date</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={3} className="px-4 py-3">Loading...</td></tr>
            ) : rows.length === 0 ? (
              <tr><td colSpan={3} className="px-4 py-3">No {label}.</td></tr>
            ) : rows.map((r, i) => (
              <tr key={r.id ?? i} className={i % 2 ? "bg-cream/60" : ""}>
                <td className="px-4 py-3">{r.head || r.title}</td>
                <td className="px-4 py-3">{r.amount}</td>
                <td className="px-4 py-3">{r.due_date || r.paid_at || r.date || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  return (
    <>
      <h1 className="font-display text-3xl font-black text-maroon">Fees</h1>
      <p className="mt-1 text-ink/80">Your fee structure and payment history.</p>
      <h2 className="mt-8 font-display text-xl font-bold text-maroon">Fee Structure</h2>
      {renderTable(feeStructure, "fee entries", "Amount")}
      <h2 className="mt-8 font-display text-xl font-bold text-maroon">Payments</h2>
      {renderTable(payments, "payments", "Amount")}
    </>
  );
}
