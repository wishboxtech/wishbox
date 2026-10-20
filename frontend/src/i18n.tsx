import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import persian from "./fa.json";

export const en = {
  tagline: "Little wishes. Big smiles.",
  mySpace: "My space",
  wishlists: "My wishlists",
  profile: "My profile",
  help: "How it works",
  contact: "Contact & support",
  language: "Language",
  english: "English",
  signIn: "Sign in",
  signOut: "Sign out",
  start: "Make a little room for joy.",
  startCopy:
    "Save the things you love. Share them with the people who love you.",
  eyebrow: "GOOD THINGS START WITH A WISH",
  hello: "Hello",
  welcome: "Welcome to your happy place.",
  welcomeCopy:
    "A home for all the things you’re wishing for. Big, small, and everything in between.",
  createList: "Create a wishlist",
  newList: "New wishlist",
  addWish: "Add a wish",
  allLists: "All wishlists",
  search: "Search your wishlists…",
  searchWishes: "Search wishes…",
  newest: "Newest first",
  oldest: "Oldest first",
  alphabetical: "Name: A–Z",
  sort: "Sort by",
  listsCount: "Wishlists",
  wishesCount: "Wishes in this list",
  shareJoy: "Made to be shared",
  shareCopy: "The best gifts start with a little hint.",
  openList: "Open wishlist",
  emptyTitle: "Your next big wish starts here.",
  emptyCopy:
    "A birthday coming up? Something you’ve had your eye on? Give it a little home.",
  noResults: "No wishes found here.",
  noResultsCopy: "Try a different search, or make something new.",
  emptyWishes: "A blank canvas for your wishes.",
  emptyWishesCopy: "Add your first wish and let the possibilities begin.",
  loginTitle: "Your wishes are waiting.",
  loginCopy: "Sign in or create an account with a one-time code.",
  phone: "Mobile number",
  phoneHint: "Use an Iranian number, like 09123456789.",
  sendCode: "Get my code",
  verify: "Let me in",
  code: "Verification code",
  codeSent: "Enter the code for",
  changeNumber: "Use another number",
  localCode: "Local development: use code 123456. No SMS is sent.",
  localMode: "Development mode",
  name: "Name",
  description: "Description",
  price: "Price",
  priceHint: "Whole numbers only. Use the same currency throughout your list.",
  listNamePlaceholder: "e.g. A birthday full of little joys",
  wishNamePlaceholder: "What are you wishing for?",
  descriptionPlaceholder: "A few details to make it yours…",
  cover: "Cover image",
  chooseImage: "Choose an image",
  removeImage: "Remove image",
  imageHint: "PNG, JPEG, GIF or WebP · up to 10 MB",
  save: "Save changes",
  create: "Create wishlist",
  createWish: "Add to my wishlist",
  cancel: "Cancel",
  close: "Close",
  edit: "Edit",
  editList: "Edit wishlist",
  editWish: "Edit wish",
  delete: "Delete",
  deleteList: "Delete wishlist",
  deleteWish: "Delete wish",
  deleteTitle: "Say goodbye to this one?",
  deleteCopy:
    "This will permanently delete it. Deleting a wishlist also removes its wishes.",
  share: "Share wishlist",
  shareWish: "Share wish",
  shareTitle: "A little hint goes a long way.",
  shareDescription:
    "Anyone with this link can see these wishes and offer a gift. Share it with someone you trust.",
  copy: "Copy link",
  copied: "Link copied!",
  publicList: "A wishlist shared with you",
  publicWish: "A little wish, just waiting",
  publicCopy: "Make someone’s day with something they’ll love.",
  reserve: "I’d like to gift this",
  reserveTitle: "You’re about to make a day.",
  nickname: "Your name or nickname",
  nicknameHint: "No account needed. Your name accompanies your gift request.",
  confirmReservation: "Send gift request",
  reserved: "Your gift request has been sent!",
  reservationNote:
    "This sends a reservation request. It does not make a purchase or payment.",
  firstName: "First name",
  lastName: "Last name",
  bio: "A little about you",
  birthdate: "Birthday",
  gender: "Gender",
  unspecified: "Prefer not to say",
  male: "Male",
  female: "Female",
  profileCopy: "Make this little corner of the internet feel like you.",
  profileSetup: "Before your first wishlist, tell us a little about yourself.",
  profileSaved: "Your profile is saved.",
  photo: "Profile photo",
  avatar: "Your avatar",
  avatarMissing:
    "No avatar has been configured for your account yet. You can upload a profile photo instead.",
  background: "Background",
  border: "Border",
  avatarSaved: "Avatar updated.",
  saved: "All saved. A little closer to your wish!",
  deleted: "Deleted successfully.",
  loading: "Gathering a little goodness…",
  retry: "Try again",
  back: "Back to wishlists",
  home: "Go to my space",
  errorTitle: "Something got in the way.",
  networkError: "We couldn’t reach Wishy. Check your connection and try again.",
  genericError:
    "We couldn’t complete that. Please check the details and try again.",
  notFound: "This wish may have moved on.",
  notFoundCopy: "The link may be incomplete, or the owner may have removed it.",
  unauthorized: "Your session has ended. Please sign in again.",
  forbidden: "You don’t have permission to change this wishlist.",
  invalidOtp:
    "That code is invalid or has expired. Please check it or request a new one.",
  otpExists:
    "A code was already requested. Use it, or wait two minutes before requesting another.",
  invalidImage: "Please choose a supported image under 10 MB.",
  required: "Please complete all required fields.",
  supportEmpty: "No contact details have been published yet.",
  stepOne: "Make it yours",
  stepOneCopy:
    "Create a wishlist for a birthday, a new chapter, or just because.",
  stepTwo: "Collect a little joy",
  stepTwoCopy:
    "Add wishes, a photo, a price, and those helpful little details.",
  stepThree: "Let good things happen",
  stepThreeCopy:
    "Send your link. Friends can explore and offer a gift without signing in.",
  helpTitle: "From “I wish” to “for you”.",
  helpCopy: "Less guessing. More thoughtful gifting.",
  collection: "A collection of possibilities",
  footer: "Made for a little more thoughtfulness.",
  explore: "Your wishes, beautifully together.",
  exploreCopy: "One place for the things that make you smile.",
  yourLists: "Your collections",
  updated: "Updated",
  view: "View",
  listView: "List view",
  gridView: "Grid view",
  ready: "Ready for a little magic?",
  readyCopy: "Your next favorite thing deserves a place here.",
  tip: "A little Wishy tip",
  tipCopy:
    "Add a few details to each wish. A thoughtful hint makes a thoughtful gift.",
  shared: "Shared wishes",
  account: "Account menu",
  owner: "Your wishlist",
  refreshing: "Refresh",
} as const;

export type TranslationKey = keyof typeof en;
export type Language = "en" | "fa";
const dictionary: Record<string, string> = persian;
export function translate(
  copy: string,
  lang: Language,
  values: Record<string, string | number> = {},
) {
  const text = lang === "fa" ? dictionary[copy.trim()] || copy : copy;
  return text.replace(/\{(\w+)\}/g, (_, key: string) =>
    String(values[key] ?? `{${key}}`),
  );
}
export function storedLanguage(): Language {
  try {
    return localStorage.getItem("wishbox.language") === "fa" ? "fa" : "en";
  } catch {
    return "en";
  }
}
export function locale() {
  return typeof document !== "undefined" &&
    document.documentElement.lang === "fa"
    ? "fa-IR"
    : "en";
}
const LanguageContext = createContext({
  lang: "en" as Language,
  setLang: (_: Language) => {},
  t: (key: TranslationKey): string => en[key],
  tr: (copy: string, values?: Record<string, string | number>) =>
    translate(copy, "en", values),
});
export function LanguageProvider({ children }: { children: ReactNode }) {
  const [lang, setLang] = useState<Language>(storedLanguage);
  useEffect(() => {
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === "fa" ? "rtl" : "ltr";
    document.title =
      lang === "fa"
        ? "ویشی — یکم راهنمایی برای هر کادویی لازمه"
        : "Wishy — Your wishes, their next great gift";
    try {
      localStorage.setItem("wishbox.language", lang);
    } catch {
      /* Locale still works without storage. */
    }
  }, [lang]);
  const value = useMemo(
    () => ({
      lang,
      setLang,
      t: (key: TranslationKey) => translate(en[key], lang),
      tr: (copy: string, values?: Record<string, string | number>) =>
        translate(copy, lang, values),
    }),
    [lang],
  );
  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
}
export const useLanguage = () => useContext(LanguageContext);
