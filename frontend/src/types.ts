export type Media = { file: string };
export type Collection = {
  id: string;
  name: string;
  description: string;
  cover: Media | null;
  created_at: string;
  updated_at: string;
};
export type Wish = Collection & { price: string; wishlist_id: string };
export type Profile = {
  profile_id: string;
  first_name: string | null;
  last_name: string | null;
  bio: string | null;
  birthdate: string | null;
  gender: string | null;
  phone_number: string | null;
  email: string | null;
  photo: Media | null;
  cat_avatar?: import("./cat").CatRecipe | null;
};
export type Avatar = {
  wrapper_shape: string;
  background: { color: string; border_color: string };
  gender: string;
  widgets: Record<string, { fill_color: string | null; image: Media | null }>;
};
export type Tokens = {
  access_token: string;
  refresh_token: string;
  is_new_user?: boolean;
  guest_claimed?: boolean;
};

export type GiftStatus =
  | "available"
  | "reserved"
  | "purchased"
  | "received"
  | "cancelled"
  | "expired";
export type Activity = {
  wish_id: string;
  views: number;
  likes: number;
  liked: boolean;
  status: GiftStatus;
  is_owner: boolean;
  is_giver: boolean;
  reservation_id?: number | null;
};
export type SharedList = {
  wishlist: Collection;
  wishes: Wish[];
  activity: Activity[];
  is_owner: boolean;
};
export type GiftRecord = {
  id: number;
  wish_id: string;
  wishlist_id: string;
  wish_name: string;
  status: GiftStatus;
  created_at: string;
  management_token?: string | null;
  purchase_by?: string | null;
  purchase_plan?: string;
  expires_at?: string | null;
  extension_count?: number;
  received_at?: string | null;
  thank_you?: string;
  thank_you_sent_at?: string | null;
  follow_up_note?: string;
  follow_up_sent_at?: string | null;
  follow_up_acknowledged_at?: string | null;
};
export type Notification = {
  id: string;
  wish_id: string | null;
  wish_name: string;
  event: string;
  read_at: string | null;
  created_at: string;
};
export type Inbox = { items: Notification[]; unread: number };

export type GiftPlan = {
  purchase_by: string;
  purchase_plan: string;
  details_checked: boolean;
  nickname?: string;
};
export type OwnerExperience = {
  role: "owner";
  gift: Pick<
    GiftRecord,
    "id" | "wish_id" | "wish_name" | "status" | "received_at"
  >;
  fit: string;
  private_note: string;
  thank_you: string;
  thank_you_sent_at: string | null;
  follow_up_note: string;
  follow_up_sent_at: string | null;
  follow_up_acknowledged_at: string | null;
};
export type GiverExperience = { role: "giver"; gift: GiftRecord };
export type GiftExperience = OwnerExperience | GiverExperience;
