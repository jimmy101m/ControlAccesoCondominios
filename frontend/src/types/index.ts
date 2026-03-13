export type RoleName = "resident" | "admin_local" | "guard";

export interface Role {
  id: string;
  name: RoleName;
}

export interface User {
  id: string;
  full_name: string;
  email: string;
  role_id: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface Invitation {
  id: string;
  resident_id: string;
  condominium_id: string;
  unit_id: string;
  token: string;
  access_mode: "pedestrian" | "vehicle";
  plate_number: string | null;
  expires_at: string;
  status:
    | "draft"
    | "sent"
    | "registered"
    | "approved"
    | "cancelled"
    | "expired"
    | "used";
  confirmed_at: string | null;
  cancelled_at: string | null;
  used_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface Visitor {
  id: string;
  full_name: string;
  phone: string;
  document_type: "INE" | "pasaporte" | "licencia";
  document_number: string;
  document_file_path: string;
  face_image_path: string;
  created_at: string;
}

export interface AccessGrant {
  id: string;
  invitation_id: string;
  visitor_id: string;
  status: "pending_sync" | "active" | "revoked" | "expired" | "used" | "sync_error";
  valid_from: string;
  valid_until: string;
  single_use: boolean;
  used_at: string | null;
  last_synced_at: string | null;
}
