import api from "./api";

export interface Transaction {
  id: number;
  transaction_id: string;
  user: number;
  user_username: string;
  sender_upi: string;
  receiver_upi: string;
  amount: string;
  transaction_type: "SEND" | "RECEIVE" | "REQUEST";
  description?: string;
  device_id?: string;
  ip_address?: string;
  location?: string;
  is_fraud: boolean;
  fraud_probability: number;
  fraud_details?: any;
  created_at: string;
  updated_at: string;
}

export interface TransactionCreate {
  sender_upi: string;
  receiver_upi: string;
  amount: number;
  transaction_type: "SEND" | "RECEIVE" | "REQUEST";
  description?: string;
  device_id?: string;
  ip_address?: string;
  location?: string;
}

export interface FraudAlert {
  id: number;
  transaction: number;
  transaction_details: Transaction;
  alert_type: string;
  severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  message: string;
  is_resolved: boolean;
  resolved_at?: string;
  created_at: string;
}

export interface DashboardStats {
  total_transactions: number;
  total_amount: number;
  fraud_transactions: number;
  fraud_amount: number;
  fraud_rate: number;
  unresolved_alerts: number;
  fraud_trend: {
    date: string;
    total: number;
    fraud: number;
  }[];
  recent_transactions: Transaction[];
}

export const transactionService = {
  async getTransactions(params?: any): Promise<Transaction[]> {
    const response = await api.get("/api/transactions/", { params });
    return response.data.results || response.data;
  },

  async createTransaction(data: TransactionCreate): Promise<Transaction> {
    const response = await api.post("/api/transactions/", data);
    return response.data;
  },

  async getTransaction(id: number): Promise<Transaction> {
    const response = await api.get(`/api/transactions/${id}/`);
    return response.data;
  },

  async getFraudAlerts(): Promise<FraudAlert[]> {
    const response = await api.get("/api/transactions/alerts/");
    return response.data.results || response.data;
  },

  async getDashboardStats(days: number = 30): Promise<DashboardStats> {
    const response = await api.get("/api/transactions/stats/", {
      params: { days },
    });
    return response.data;
  },
};
