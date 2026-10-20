import { useLanguage } from "./i18n";
import {
  useCallback,
  useEffect,
  useRef,
  useState,
  type ReactNode,
} from "react";
import {
  ArrowLeft,
  ArrowRight,
  Bell,
  Check,
  CheckCheck,
  Copy,
  Eye,
  Gift,
  Heart,
  Link,
  LoaderCircle,
  LogOut,
  Pencil,
  Plus,
  Search,
  Share2,
  Sparkles,
  Trash2,
  UserRound,
  X,
} from "lucide-react";
import { ApiError, mediaUrl, request, session } from "./api";
import { Empty, ErrorMessage, Loading, Modal } from "./components";
import { AuthModal, ResourceForm } from "./forms";
import { CommitmentForm, GiftJourney, getGiftExperience } from "./GiftJourney";
import { CatAvatar } from "./CatAvatar";
import { ContactPage } from "./ContactPage";
import { ProfilePage } from "./ProfilePage";
import {
  getActivity,
  giftActions,
  giftHeaders,
  guestKey,
  localGifts,
  rememberGift,
  statusLabels,
} from "./gifting";
import type {
  Activity,
  Collection,
  GiftRecord,
  GiftPlan,
  Inbox,
  Profile,
  SharedList,
  Wish,
} from "./types";

type Editor = {
  kind: "list" | "wish";
  item?: Collection | Wish;
  listId?: string;
};
function useRoute() {
  const [path, setPath] = useState(window.location.pathname);
  useEffect(() => {
    const listener = () => setPath(window.location.pathname);
    window.addEventListener("popstate", listener);
    return () => window.removeEventListener("popstate", listener);
  }, []);
  const navigate = useCallback((next: string) => {
    window.history.pushState({}, "", next);
    setPath(next);
    window.scrollTo({ top: 0 });
  }, []);
  return [path, navigate] as const;
}
export function Cat({ large = false }: { large?: boolean }) {
  const { tr } = useLanguage();
  return (
    <span className={`cat-logo ${large ? "cat-large" : ""}`}>
      <img
        src="/wishy-cat.jpg"
        alt={large ? tr("Wishy, our purple wishing cat") : ""}
      />
    </span>
  );
}
function Cover({ item, onClick }: { item: Collection; onClick?: () => void }) {
  const { tr } = useLanguage();
  const [broken, setBroken] = useState(false);
  const content =
    item.cover && !broken ? (
      <img
        src={mediaUrl(item.cover.file)}
        alt=""
        loading="lazy"
        onError={() => setBroken(true)}
      />
    ) : (
      <>
        <Gift size={48} strokeWidth={1.4} />
        <span className="cover-spark">✦</span>
      </>
    );
  return onClick ? (
    <button
      className="card-cover"
      aria-label={tr("Open {name}", { name: item.name })}
      onClick={onClick}
    >
      {content}
    </button>
  ) : (
    <div className="card-cover detail-cover">{content}</div>
  );
}
const money = (value: string, lang: string) =>
  new Intl.NumberFormat(lang, { maximumFractionDigits: 0 }).format(
    Number(value),
  );
const messages: Record<string, string> = {
  reserved: "Someone is making your wish happen",
  purchased: "Your gift is on its way",
  received: "You confirmed a wish came true",
  cancelled: "A reservation was released",
  thank_you: "Your gift was received",
  gift_received: "Your gift arrived — a thoughtful plan completed",
  thanks_shared: "A personal note from your friend",
  follow_up_shared: "Your friend shared a practical note about the gift",
  follow_up_seen: "Your friend has seen your practical note",
  hold_released: "This wish is available again",
  hold_expired: "Your gift hold has ended — you can plan again when ready",
  plan_reminder: "A gentle check-in on your gift plan",
};

export function App() {
  const { tr, lang, setLang } = useLanguage();
  const [path, navigate] = useRoute();
  const [signedIn, setSignedIn] = useState(!!session.get());
  const [profile, setProfile] = useState<Profile | null>(null);
  const [profileReady, setProfileReady] = useState(false);
  const [profileAttempt, setProfileAttempt] = useState(0);
  const [profileError, setProfileError] = useState<unknown>(null);
  const [lists, setLists] = useState<Collection[]>([]);
  const [shared, setShared] = useState<SharedList | null>(null);
  const [wish, setWish] = useState<Wish | null>(null);
  const [activity, setActivity] = useState<Activity | null>(null);
  const [gifts, setGifts] = useState<GiftRecord[]>([]);
  const [inbox, setInbox] = useState<Inbox>({ items: [], unread: 0 });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<unknown>(null);
  const [revision, setRevision] = useState(0);
  const [search, setSearch] = useState("");
  const [auth, setAuth] = useState(false);
  const [editor, setEditor] = useState<Editor | null>(null);
  const [shareLink, setShareLink] = useState("");
  const [copied, setCopied] = useState(false);
  const [deleting, setDeleting] = useState<{
    name: string;
    url: string;
    parent: string;
  } | null>(null);
  const [deleteBusy, setDeleteBusy] = useState(false);
  const [modalError, setModalError] = useState<unknown>(null);
  const [toast, setToast] = useState("");
  const [account, setAccount] = useState(false);
  const accountButton = useRef<HTMLButtonElement>(null);
  useEffect(() => {
    if (!account) return;
    const closeMenu = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setAccount(false);
        accountButton.current?.focus();
      }
    };
    document.addEventListener("keydown", closeMenu);
    return () => document.removeEventListener("keydown", closeMenu);
  }, [account]);
  const pendingCreate = useRef(false);
  const listMatch = path.match(/^\/(?:lists|shared)\/([a-f\d-]+)\/?$/i);
  const wishMatch = path.match(/^\/wish\/([a-f\d-]+)(?:\/gift\/(\d+))?\/?$/i);
  const listId = listMatch?.[1],
    wishId = wishMatch?.[1];
  const refresh = useCallback(() => setRevision((v) => v + 1), []);

  useEffect(() => {
    const logout = () => {
      setSignedIn(false);
      setProfile(null);
      setProfileReady(false);
      setLists([]);
      setInbox({ items: [], unread: 0 });
      setAccount(false);
      pendingCreate.current = false;
      refresh();
    };
    window.addEventListener("wishbox:logout", logout);
    return () => window.removeEventListener("wishbox:logout", logout);
  }, [refresh]);
  useEffect(() => {
    if (!toast) return;
    const timer = setTimeout(() => setToast(""), 4500);
    return () => clearTimeout(timer);
  }, [toast]);
  useEffect(() => {
    setSearch("");
    setAccount(false);
    setModalError(null);
  }, [path]);
  useEffect(() => {
    if (!signedIn) return;
    const controller = new AbortController();
    setProfileReady(false);
    setProfileError(null);
    request<Profile>("profile/", { signal: controller.signal })
      .then((value) => {
        if (!controller.signal.aborted) setProfile(value);
      })
      .catch((err) => {
        if (controller.signal.aborted) return;
        if (err instanceof ApiError && err.status === 404) setProfile(null);
        else setProfileError(err);
      })
      .finally(() => {
        if (!controller.signal.aborted) setProfileReady(true);
      });
    return () => controller.abort();
  }, [signedIn, profileAttempt]);
  useEffect(() => {
    if (!signedIn || !profile) return;
    const controller = new AbortController();
    const load = () => {
      if (!document.hidden)
        request<Inbox>("notifications/", { signal: controller.signal })
          .then((value) => {
            if (!controller.signal.aborted) setInbox(value);
          })
          .catch(() => {});
    };
    load();
    const timer = setInterval(load, 30000);
    document.addEventListener("visibilitychange", load);
    return () => {
      controller.abort();
      clearInterval(timer);
      document.removeEventListener("visibilitychange", load);
    };
  }, [signedIn, profile, revision]);
  useEffect(() => {
    if (pendingCreate.current && profile) {
      pendingCreate.current = false;
      setEditor({ kind: "list" });
    }
  }, [profile]);
  useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;
    setError(null);
    setLoading(true);
    setShared(null);
    setWish(null);
    setActivity(null);
    async function load() {
      if (listId)
        setShared(
          await request<SharedList>(`wishlist/${listId}/shared/`, {
            headers: giftHeaders(),
            signal,
          }),
        );
      else if (wishId) {
        const [item, stats] = await Promise.all([
          request<Wish>(`wish/${wishId}/`, { signal }),
          getActivity(wishId, "view", signal),
        ]);
        if (!signal.aborted) {
          setWish(item);
          setActivity(stats);
        }
      } else if (path === "/gifts") {
        const registered = signedIn
          ? await request<GiftRecord[]>("gifts/", { signal })
          : [];
        const guest = await Promise.all(
          localGifts().map(async (gift) => {
            try {
              const experience = await getGiftExperience(
                gift.id,
                gift.wish_id,
                signal,
              );
              return experience.role === "giver"
                ? { ...gift, ...experience.gift }
                : gift;
            } catch (err) {
              if (
                err instanceof ApiError &&
                (err.status === 404 || err.status === 400)
              )
                return { ...gift, status: "cancelled" as const };
              throw err;
            }
          }),
        );
        const unique = new Map(guest.map((gift) => [gift.id, gift]));
        registered.forEach((gift) => unique.set(gift.id, gift));
        if (!signal.aborted)
          setGifts(
            [...unique.values()].sort((a, b) =>
              b.created_at.localeCompare(a.created_at),
            ),
          );
      } else if (path === "/notifications" && signedIn)
        setInbox(await request<Inbox>("notifications/", { signal }));
      else if (path === "/" && signedIn && profile)
        setLists(await request<Collection[]>("profile/wishlist/", { signal }));
    }
    load()
      .catch((err) => {
        if (!signal.aborted) setError(err);
      })
      .finally(() => {
        if (!signal.aborted) setLoading(false);
      });
    return () => controller.abort();
  }, [path, listId, wishId, signedIn, profile, revision]);

  function createList() {
    if (!signedIn) {
      pendingCreate.current = true;
      setAuth(true);
    } else if (!profile) {
      pendingCreate.current = true;
      navigate("/profile");
    } else setEditor({ kind: "list" });
  }
  function share(id: string, kind: "list" | "wish") {
    setCopied(false);
    setModalError(null);
    setShareLink(
      `${window.location.origin}/${kind === "list" ? "shared" : "wish"}/${id}`,
    );
  }
  async function remove() {
    if (!deleting) return;
    setDeleteBusy(true);
    setModalError(null);
    try {
      await request(deleting.url, { method: "DELETE" });
      navigate(deleting.parent);
      setDeleting(null);
      refresh();
      setToast(tr("Removed from your wishes."));
    } catch (err) {
      setModalError(err);
    } finally {
      setDeleteBusy(false);
    }
  }
  function backButton() {
    return (
      <button className="text-button back-link" onClick={() => navigate("/")}>
        <ArrowLeft className="directional" size={18} />
        {tr("My wishlists")}
      </button>
    );
  }
  const shownLists = lists.filter((item) =>
    item.name.toLowerCase().includes(search.toLowerCase()),
  );
  const shownWishes =
    shared?.wishes.filter((item) =>
      `${item.name} ${item.description}`
        .toLowerCase()
        .includes(search.toLowerCase()),
    ) || [];
  const isHome = path === "/";
  const pageKnown =
    isHome ||
    listId ||
    wishId ||
    ["/gifts", "/notifications", "/profile", "/help", "/contact"].includes(
      path,
    );
  let body: ReactNode;
  if (loading || (signedIn && !profileReady && isHome)) body = <Loading />;
  else if (error)
    body = (
      <div className="error-state">
        <Cat />
        <h1>{tr("We hit a little bump.")}</h1>
        <ErrorMessage error={error} />
        <button className="button primary" onClick={refresh}>
          {tr("Try again")}
        </button>
        {backButton()}
      </div>
    );
  else if (!pageKnown)
    body = (
      <Empty
        title={tr("This page wandered off.")}
        copy={tr("Head back to your wishlists to find your next little joy.")}
        action={() => navigate("/")}
        label={tr("Go home")}
      />
    );
  else if (path === "/profile")
    body = signedIn ? (
      <>
        <ErrorMessage error={profileError} />
        {!!profileError && (
          <button
            className="button secondary"
            onClick={() => setProfileAttempt((value) => value + 1)}
          >
            {tr("Retry loading profile")}
          </button>
        )}
        {profileReady ? (
          <ProfilePage
            profile={profile}
            complete={(p) => {
              setProfile(p);
              navigate("/");
              refresh();
            }}
            notify={setToast}
          />
        ) : (
          <Loading />
        )}
      </>
    ) : (
      <Empty
        title={tr("A little space of your own.")}
        copy={tr("Sign in to make and share your wishlist.")}
        action={() => setAuth(true)}
        label={tr("Sign in")}
      />
    );
  else if (listId && shared) {
    const granted = shared.activity.filter(
      (item) => item.status === "received",
    ).length;
    body = (
      <>
        {backButton()}
        <div className="page-heading heading-with-actions">
          <div>
            <span className="eyebrow">
              {shared.is_owner
                ? tr("YOUR WISHLIST")
                : tr("A LITTLE HINT FOR A GREAT GIFT")}
            </span>
            <h1 dir="auto">{shared.wishlist.name}</h1>
            {shared.wishlist.description && (
              <p>{shared.wishlist.description}</p>
            )}
            <div className="list-progress">
              <span>
                {tr("{count} wishes", {
                  count: new Intl.NumberFormat(lang).format(
                    shared.wishes.length,
                  ),
                })}
              </span>
              <span>·</span>
              <span>
                {tr("{count} received", {
                  count: new Intl.NumberFormat(lang).format(granted),
                })}
              </span>
              {granted > 0 && <Sparkles size={16} />}
            </div>
          </div>
          <div className="heading-actions">
            <button
              className="button secondary"
              onClick={() => share(listId, "list")}
            >
              <Share2 size={18} />
              {tr("Share list")}
            </button>
            {shared.is_owner && (
              <button
                className="button primary"
                onClick={() => setEditor({ kind: "wish", listId: listId })}
              >
                <Plus size={19} />
                {tr("Add a wish")}
              </button>
            )}
          </div>
        </div>
        {!shared.is_owner && (
          <div className="friendly-note">
            <Gift size={22} />
            <span>
              {tr(
                "Pick a wish, reserve it, and make their day. Everyone sees when a gift is taken.",
              )}
            </span>
          </div>
        )}
        {shared.wishes.length > 0 && (
          <SearchField
            value={search}
            set={setSearch}
            placeholder={tr("Find a wish…")}
          />
        )}
        {shownWishes.length ? (
          <div className="wish-grid">
            {shownWishes.map((item) => (
              <WishCard
                key={item.id}
                item={item}
                activity={shared.activity.find(
                  (stat) => stat.wish_id === item.id,
                )}
                open={() => navigate(`/wish/${item.id}`)}
              />
            ))}
          </div>
        ) : (
          <Empty
            title={
              search
                ? tr("No wishes match just yet.")
                : shared.is_owner
                  ? tr("What’s on your wish list?")
                  : tr("Good things are coming.")
            }
            copy={
              search
                ? tr("Try another name.")
                : shared.is_owner
                  ? tr(
                      "Something useful, something fun, something just because. Add your first wish.",
                    )
                  : tr(
                      "This wishlist is waiting for its first wish. Check back soon.",
                    )
            }
            action={
              shared.is_owner && !search
                ? () => setEditor({ kind: "wish", listId: listId })
                : undefined
            }
            label={tr("Add your first wish")}
          />
        )}
        {shared.is_owner && (
          <div className="list-settings">
            <button
              className="text-button"
              onClick={() => setEditor({ kind: "list", item: shared.wishlist })}
            >
              <Pencil size={16} />
              {tr("Edit list")}
            </button>
            <button
              className="text-button danger"
              onClick={() => {
                setModalError(null);
                setDeleting({
                  name: shared.wishlist.name,
                  url: `wishlist/${listId}/`,
                  parent: "/",
                });
              }}
            >
              <Trash2 size={16} />
              {tr("Delete list")}
            </button>
          </div>
        )}
      </>
    );
  } else if (wish && activity)
    body = (
      <>
        <button
          className="text-button back-link"
          onClick={() => navigate(`/shared/${wish.wishlist_id}`)}
        >
          <ArrowLeft className="directional" size={18} />
          {tr("Back to wishlist")}
        </button>
        <WishDetail
          key={`${wish.id}:${revision}`}
          wish={wish}
          openCurrent={() => navigate(`/wish/${wish.id}`)}
          initial={activity}
          reservationId={wishMatch?.[2] ? Number(wishMatch[2]) : undefined}
          signedIn={signedIn && !!profile}
          share={() => share(wish.id, "wish")}
          refresh={refresh}
          notify={setToast}
        />
        {activity.is_owner && (
          <div className="list-settings">
            <button
              className="text-button"
              onClick={() => navigate(`/lists/${wish.wishlist_id}`)}
            >
              <ArrowLeft className="directional" size={16} />
              {tr("Back to this wishlist")}
            </button>
            <OwnerWishActions
              wish={wish}
              edit={(parent) =>
                setEditor({ kind: "wish", item: wish, listId: parent })
              }
              remove={(parent) => {
                setModalError(null);
                setDeleting({
                  name: wish.name,
                  url: `wishlist/${parent}/wish/${wish.id}/`,
                  parent: `/lists/${parent}`,
                });
              }}
            />
          </div>
        )}
      </>
    );
  else if (path === "/gifts")
    body = (
      <>
        <div className="page-heading">
          <span className="eyebrow">
            {tr("A LITTLE THOUGHT GOES A LONG WAY")}
          </span>
          <h1>{tr("Gifts I’m giving")}</h1>
          <p>
            {tr(
              "Your thoughtful plans, from a small promise to a gift received.",
            )}
          </p>
        </div>
        {!signedIn && (
          <p className="notice">
            {tr(
              "Guest gifts are saved in this browser. Keep this browser’s data to manage them.",
            )}
          </p>
        )}
        {gifts.some((gift) => gift.status === "received") && (
          <div className="kindness-summary">
            <Cat />
            <div>
              <span className="eyebrow">{tr("YOUR LITTLE KEEPSAKES")}</span>
              <h2>
                {tr("{count} gifts received by your people", {
                  count: new Intl.NumberFormat(lang).format(
                    gifts.filter((gift) => gift.status === "received").length,
                  ),
                })}
              </h2>
              <p>
                {tr(
                  "Real gifts, confirmed by their recipients. Every shared note belongs to the two of you.",
                )}
              </p>
            </div>
          </div>
        )}
        {gifts.length ? (
          <div className="gift-list">
            {gifts.map((gift) => (
              <button
                className="gift-row"
                key={gift.id}
                onClick={() =>
                  navigate(`/wish/${gift.wish_id}/gift/${gift.id}`)
                }
              >
                <span className="round-icon">
                  <Gift size={24} />
                </span>
                <span>
                  <strong dir="auto">{gift.wish_name}</strong>
                  <span className={`status status-${gift.status}`}>
                    {tr(statusLabels[gift.status])}
                  </span>
                  {gift.purchase_by && gift.status === "reserved" && (
                    <span className="gift-row-plan">
                      {tr("Your plan: {plan} · by {date}", {
                        plan: tr(gift.purchase_plan || ""),
                        date: new Intl.DateTimeFormat(lang, {
                          dateStyle: "medium",
                        }).format(new Date(`${gift.purchase_by}T12:00:00`)),
                      })}
                    </span>
                  )}
                  {gift.thank_you && (
                    <span className="keepsake-note">“{gift.thank_you}”</span>
                  )}
                  {gift.follow_up_note && (
                    <span className="gift-row-plan">
                      {gift.follow_up_acknowledged_at
                        ? tr("You’ve seen your friend’s practical note")
                        : tr("A practical note from your friend")}
                    </span>
                  )}
                </span>
                <ArrowRight className="directional" size={20} />
              </button>
            ))}
          </div>
        ) : (
          <Empty
            title={tr("Someone’s next favorite thing.")}
            copy={tr(
              "Open a friend’s wishlist link and reserve something they’ll love. Your gifts will appear here.",
            )}
          />
        )}
      </>
    );
  else if (path === "/notifications")
    body = (
      <>
        <div className="page-heading heading-with-actions">
          <div>
            <span className="eyebrow">{tr("GOOD NEWS LIVES HERE")}</span>
            <h1>
              {tr("Notifications")}
              {inbox.unread > 0 && (
                <span className="count-pill">{inbox.unread}</span>
              )}
            </h1>
            <p>{tr("Little updates on the wishes that matter to you.")}</p>
          </div>
          {inbox.unread > 0 && (
            <button
              className="button secondary"
              onClick={async () => {
                try {
                  setInbox(
                    await request<Inbox>("notifications/", {
                      method: "PATCH",
                      body: {},
                    }),
                  );
                } catch (err) {
                  setError(err);
                }
              }}
            >
              <CheckCheck size={18} />
              {tr("Mark all read")}
            </button>
          )}
        </div>
        {!signedIn ? (
          <Empty
            title={tr("Your good-news corner.")}
            copy={tr("Sign in to see updates on your wishlists.")}
            action={() => setAuth(true)}
            label={tr("Sign in")}
          />
        ) : inbox.items.length ? (
          <div className="notification-list">
            {inbox.items.map((item) => (
              <div
                className={`notification ${item.read_at ? "" : "unread"}`}
                key={item.id}
              >
                <span className="round-icon">
                  <Gift size={24} />
                </span>
                <button
                  className="notification-content"
                  disabled={!item.wish_id}
                  onClick={async () => {
                    try {
                      setInbox(
                        await request<Inbox>("notifications/", {
                          method: "PATCH",
                          body: { notification_id: item.id },
                        }),
                      );
                      if (item.wish_id) navigate(`/wish/${item.wish_id}`);
                    } catch (err) {
                      setError(err);
                    }
                  }}
                >
                  <strong>
                    {tr(messages[item.event] || "An update on your wish")}
                  </strong>
                  <span>
                    {item.wish_name}
                    {!item.wish_id ? tr(" · Wish removed") : ""}
                  </span>
                  <time>
                    {new Intl.DateTimeFormat(lang, {
                      dateStyle: "medium",
                      timeStyle: "short",
                    }).format(new Date(item.created_at))}
                  </time>
                </button>
                {!item.read_at && (
                  <button
                    className="icon-button"
                    aria-label={tr("Mark notification about {name} as read", {
                      name: item.wish_name,
                    })}
                    onClick={async () => {
                      try {
                        setInbox(
                          await request<Inbox>("notifications/", {
                            method: "PATCH",
                            body: { notification_id: item.id },
                          }),
                        );
                      } catch (err) {
                        setError(err);
                      }
                    }}
                  >
                    <Check size={20} />
                  </button>
                )}
              </div>
            ))}
          </div>
        ) : (
          <Empty
            title={tr("A little quiet, for now.")}
            copy={tr(
              "We’ll let you know when a friend reserves a wish, buys your gift, or a wish comes true.",
            )}
          />
        )}
      </>
    );
  else if (path === "/contact") body = <ContactPage />;
  else if (path === "/help")
    body = (
      <>
        <div className="page-heading">
          <span className="eyebrow">{tr("LESS GUESSING, MORE GIFTING")}</span>
          <h1>{tr("From “I wish” to “for you”.")}</h1>
          <p>{tr("Just a little hint. A much better gift.")}</p>
        </div>
        <HowItWorks />
        <div className="panel help-details">
          <h2>{tr("A reservation is a promise, not a purchase.")}</h2>
          <p>
            {tr(
              "Reserve a wish so other friends know it’s taken. Buy it wherever you like, then select “I’ve bought it”. The wishlist owner confirms when it arrives.",
            )}
          </p>
          <h2>{tr("Changed your mind?")}</h2>
          <p>
            {tr(
              "Cancel your reservation from the wish or Gifts I’m giving. It becomes available for another friend. Once the owner confirms receipt, the gift is complete.",
            )}
          </p>
          <h2>{tr("What counts as a view or a like?")}</h2>
          <p>
            {tr(
              "Each browser or signed-in account counts once per wish. You can like and unlike whenever you want.",
            )}
          </p>
          <h2>{tr("Sharing and guest gifts")}</h2>
          <p>
            {tr(
              "Anyone with a wishlist link can see it. Guests can reserve without an account. Their private management key stays in this browser, so keep its data to manage a guest reservation.",
            )}
          </p>
        </div>
      </>
    );
  else if (isHome)
    body = (
      <>
        {!signedIn ? (
          <>
            <section className="hero">
              <div>
                <span className="eyebrow">
                  <Sparkles size={16} />
                  {tr("LITTLE WISHES. BIG SMILES.")}
                </span>
                <h1>
                  {tr("Good gifts start")}
                  <br />
                  {tr("with a little")} <span>{tr("hint.")}</span>
                </h1>
                <p>
                  {tr("One happy home for the things you’d love.")}
                  <br className="desktop-only" />
                  {tr("Share your wishes. Let your friends do the magic.")}
                </p>
                <button className="button primary large" onClick={createList}>
                  <Plus size={21} />
                  {tr("Make my wishlist")}
                  <ArrowRight className="directional" size={20} />
                </button>
                <span className="hero-caption">
                  {tr("Free to wish. Easy to share. Lovely to give.")}
                </span>
              </div>
              <div className="hero-art">
                <span className="orbit-text">
                  {tr("your next little joy ✦")}
                </span>
                <Cat large />
                <span className="floating-label">
                  <Heart size={18} fill="currentColor" />
                  {tr("A wish come true")}
                </span>
              </div>
            </section>
            <HowItWorks />
          </>
        ) : (
          <>
            <div className="page-heading heading-with-actions">
              <div>
                <span className="eyebrow">{tr("YOUR LITTLE HAPPY PLACE")}</span>
                <h1>
                  {profile?.first_name
                    ? tr("{name}’s wishlists", { name: profile.first_name })
                    : tr("My wishlists")}
                  <span className="heading-star">✦</span>
                </h1>
                <p>
                  {tr("Save what you love. Give your friends a little hint.")}
                </p>
              </div>
              <button className="button primary" onClick={createList}>
                <Plus size={19} />
                {tr("New wishlist")}
              </button>
            </div>
            <ErrorMessage error={profileError} />
            {!!profileError && (
              <button
                className="button secondary"
                onClick={() => setProfileAttempt((value) => value + 1)}
              >
                {tr("Retry loading profile")}
              </button>
            )}
            {!profile && profileReady && !profileError && (
              <div className="friendly-note">
                <Cat />
                <span>{tr("Add your name to start your first wishlist.")}</span>
                <button
                  className="button primary"
                  onClick={() => navigate("/profile")}
                >
                  {tr("Set up profile")}
                  <ArrowRight className="directional" size={17} />
                </button>
              </div>
            )}
            {lists.length > 0 && (
              <SearchField
                value={search}
                set={setSearch}
                placeholder={tr("Find a wishlist…")}
              />
            )}
            {shownLists.length ? (
              <div className="wish-grid">
                {shownLists.map((item) => (
                  <article className="collection-card" key={item.id}>
                    <Cover
                      item={item}
                      onClick={() => navigate(`/lists/${item.id}`)}
                    />
                    <div className="card-body">
                      <button
                        className="card-title"
                        onClick={() => navigate(`/lists/${item.id}`)}
                      >
                        {item.name}
                      </button>
                      <p>{item.description || tr("A few things I’d love.")}</p>
                      <div className="card-footer">
                        <button
                          className="text-button"
                          onClick={() => navigate(`/lists/${item.id}`)}
                        >
                          {tr("Open list")}
                          <ArrowRight className="directional" size={17} />
                        </button>
                        <button
                          className="icon-button"
                          aria-label={tr("Share {name}", { name: item.name })}
                          onClick={() => share(item.id, "list")}
                        >
                          <Share2 size={19} />
                        </button>
                      </div>
                    </div>
                  </article>
                ))}
                <button className="new-list-card" onClick={createList}>
                  <span className="round-icon">
                    <Plus size={26} />
                  </span>
                  <strong>{tr("Room for one more wish")}</strong>
                  <span>{tr("Make a new wishlist")}</span>
                </button>
              </div>
            ) : (
              <Empty
                title={
                  search
                    ? tr("No matching wishlists.")
                    : tr("Big dreams. Little wishes. Start here.")
                }
                copy={
                  search
                    ? tr("Try another name.")
                    : tr(
                        "Birthday favorites, everyday joys, or that one thing you keep thinking about.",
                      )
                }
                action={createList}
                label={tr("Make my first wishlist")}
              />
            )}
          </>
        )}
      </>
    );
  return (
    <div className="app-shell">
      <a href="#main" className="skip-link">
        {tr("Skip to content")}
      </a>
      <header className="site-header">
        <div className="header-inner">
          <button
            className="brand"
            onClick={() => navigate("/")}
            aria-label={tr("Wishy home")}
          >
            <Cat />
            <span>
              {lang === "fa" ? (
                <span className="persian-wordmark">ویشی</span>
              ) : (
                "wishy"
              )}
              <span className="brand-dot">✦</span>
            </span>
          </button>
          <nav aria-label={tr("Main navigation")}>
            <button
              className={isHome || listId ? "nav-active" : ""}
              onClick={() => navigate("/")}
            >
              {tr("My wishlists")}
            </button>
            <button
              className={path === "/gifts" ? "nav-active" : ""}
              onClick={() => navigate("/gifts")}
            >
              <Gift size={18} />
              <span>{tr("Gifts I’m giving")}</span>
            </button>
          </nav>
          <div className="account-actions">
            <label className="language-switch">
              <span className="sr-only">{tr("Language")}</span>
              <select
                aria-label={tr("Language")}
                value={lang}
                onChange={(event) => setLang(event.target.value as "en" | "fa")}
              >
                <option value="en" lang="en">
                  EN
                </option>
                <option value="fa" lang="fa">
                  فارسی
                </option>
              </select>
            </label>
            {signedIn ? (
              <>
                <button
                  className={`icon-button notification-bell ${path === "/notifications" ? "nav-active" : ""}`}
                  aria-label={tr("Notifications")}
                  onClick={() => navigate("/notifications")}
                >
                  <Bell size={23} />
                  {inbox.unread > 0 && (
                    <span className="notification-dot">
                      {inbox.unread > 9 ? "9+" : inbox.unread}
                    </span>
                  )}
                </button>
                <div className="account-wrapper">
                  <button
                    className="profile-button"
                    ref={accountButton}
                    aria-label={tr("Account menu")}
                    aria-expanded={account}
                    onClick={() => setAccount(!account)}
                  >
                    {profile?.cat_avatar ? (
                      <CatAvatar recipe={profile.cat_avatar} />
                    ) : profile?.photo ? (
                      <img src={mediaUrl(profile.photo.file)} alt="" />
                    ) : (
                      <UserRound size={22} />
                    )}
                  </button>
                  {account && (
                    <>
                      <button
                        className="menu-dismiss"
                        aria-label={tr("Close account menu")}
                        onClick={() => setAccount(false)}
                      />
                      <div className="account-menu">
                        <button onClick={() => navigate("/profile")}>
                          <UserRound size={18} />
                          {tr("Your profile")}
                        </button>
                        <button
                          onClick={() => {
                            session.clear();
                            navigate("/");
                          }}
                        >
                          <LogOut size={18} />
                          {tr("Sign out")}
                        </button>
                      </div>
                    </>
                  )}
                </div>
              </>
            ) : (
              <button
                className="button secondary"
                onClick={() => setAuth(true)}
              >
                {tr("Sign in")}
                <ArrowRight className="directional" size={17} />
              </button>
            )}
          </div>
        </div>
      </header>
      <main id="main" className="main-content">
        {body}
      </main>
      <footer>
        <button className="footer-brand" onClick={() => navigate("/")}>
          {lang === "fa" ? (
            <span className="persian-wordmark">ویشی</span>
          ) : (
            "wishy"
          )}
          <span>✦</span>
        </button>
        <span>{tr("Small hints. Thoughtful gifts.")}</span>
        <button className="text-button" onClick={() => navigate("/contact")}>
          {tr("Contact & support")}
        </button>
        <button className="text-button" onClick={() => navigate("/help")}>
          {tr("How it works")}
          <ArrowRight className="directional" size={16} />
        </button>
      </footer>
      {auth && (
        <AuthModal
          close={() => {
            setAuth(false);
            pendingCreate.current = false;
          }}
          complete={() => {
            setAuth(false);
            setSignedIn(true);
            if (pendingCreate.current) navigate("/profile");
            refresh();
          }}
        />
      )}
      {editor && (
        <ResourceForm
          {...editor}
          close={() => setEditor(null)}
          complete={(result) => {
            setEditor(null);
            if (editor.kind === "list" && !editor.item)
              navigate(`/lists/${result.id}`);
            refresh();
            setToast(
              editor.item
                ? tr("All saved.")
                : editor.kind === "wish"
                  ? tr("One wish closer to a happy surprise.")
                  : tr("Your wishlist is ready. Add your first wish!"),
            );
          }}
        />
      )}
      {shareLink && (
        <Modal
          title={tr("A little hint goes a long way.")}
          close={() => setShareLink("")}
        >
          <div className="share-illustration">
            <Cat />
          </div>
          <p className="modal-copy">
            {tr(
              "Send this link to your people. They can pick a wish and reserve a gift, with or without an account.",
            )}
          </p>
          <label>
            {tr("Anyone with this link can see these wishes")}
            <input
              readOnly
              dir="ltr"
              value={shareLink}
              onFocus={(e) => e.target.select()}
            />
          </label>
          <button
            className="button primary full"
            onClick={async () => {
              try {
                await navigator.clipboard.writeText(shareLink);
                setCopied(true);
              } catch {
                setModalError(
                  new Error(tr("Copy the link from the field above.")),
                );
              }
            }}
          >
            {copied ? <Check size={19} /> : <Copy size={19} />}
            {copied ? tr("Link copied!") : tr("Copy link")}
          </button>
          {typeof navigator.share === "function" && (
            <button
              className="button secondary full"
              onClick={() => {
                navigator
                  .share({ title: tr("A little Wishy hint"), url: shareLink })
                  .catch(() => {});
              }}
            >
              <Share2 size={18} />
              {tr("Share with a friend")}
            </button>
          )}
          <ErrorMessage error={modalError} />
        </Modal>
      )}
      {deleting && (
        <Modal
          title={tr("Delete “{name}”?", { name: deleting.name })}
          close={() => {
            if (!deleteBusy) setDeleting(null);
          }}
        >
          <p className="modal-copy">
            {tr("This permanently removes it")}
            {deleting.url.includes("/wish/") ? "" : tr(" and its wishes")}
            {tr(", including gift reservations. This can’t be undone.")}
          </p>
          <ErrorMessage error={modalError} />
          <div className="form-actions">
            <button
              className="button secondary"
              disabled={deleteBusy}
              onClick={() => setDeleting(null)}
            >
              {tr("Keep it")}
            </button>
            <button
              className="button destructive"
              disabled={deleteBusy}
              onClick={remove}
            >
              {deleteBusy ? tr("Removing…") : tr("Delete")}
            </button>
          </div>
        </Modal>
      )}
      {toast && (
        <div className="toast" role="status">
          <Check size={20} />
          {toast}
          <button
            className="icon-button"
            onClick={() => setToast("")}
            aria-label={tr("Dismiss message")}
          >
            <X size={18} />
          </button>
        </div>
      )}
    </div>
  );
}

function SearchField({
  value,
  set,
  placeholder,
}: {
  value: string;
  set: (value: string) => void;
  placeholder: string;
}) {
  return (
    <label className="search-field">
      <Search size={20} />
      <input
        type="search"
        aria-label={placeholder}
        value={value}
        onChange={(e) => set(e.target.value)}
        placeholder={placeholder}
      />
    </label>
  );
}
function HowItWorks() {
  const { tr, lang } = useLanguage();
  return (
    <section className="how-it-works" aria-label={tr("How it works")}>
      {[
        {
          icon: <Plus />,
          title: tr("Make a little wish"),
          copy: tr("Save the things you’d love in one simple list."),
        },
        {
          icon: <Link />,
          title: tr("Drop a happy hint"),
          copy: tr("Share your link with your favorite people."),
        },
        {
          icon: <Gift />,
          title: tr("Let the magic happen"),
          copy: tr("Friends reserve a gift. You get a happy surprise."),
        },
      ].map((step, i) => (
        <div key={step.title}>
          <span className="step-number">
            {new Intl.NumberFormat(lang, { minimumIntegerDigits: 2 }).format(
              i + 1,
            )}
          </span>
          <span className="round-icon">{step.icon}</span>
          <h2>{step.title}</h2>
          <p>{step.copy}</p>
        </div>
      ))}
    </section>
  );
}
function WishCard({
  item,
  activity,
  open,
}: {
  item: Wish;
  activity?: Activity;
  open: () => void;
}) {
  const { tr, lang } = useLanguage();
  return (
    <article className="collection-card">
      <Cover item={item} onClick={open} />
      <div className="card-body">
        <span className={`status status-${activity?.status || "available"}`}>
          {tr(statusLabels[activity?.status || "available"])}
        </span>
        <button className="card-title" onClick={open}>
          {item.name}
        </button>
        <p className="wish-price">
          {money(item.price, lang)}
          <span>{tr("estimated price")}</span>
        </p>
        <div className="card-footer">
          <span className="mini-stats">
            <span>
              <Heart size={16} />
              {activity?.likes || 0}
            </span>
            <span>
              <Eye size={17} />
              {activity?.views || 0}
            </span>
          </span>
          <button className="text-button" onClick={open}>
            {activity?.is_owner
              ? tr("View wish")
              : activity?.status === "available"
                ? tr("Gift this")
                : tr("View details")}
            <ArrowRight className="directional" size={17} />
          </button>
        </div>
      </div>
    </article>
  );
}
// Wish responses include the parent for direct owner links.
function OwnerWishActions({
  wish,
  edit,
  remove,
}: {
  wish: Wish;
  edit: (parent: string) => void;
  remove: (parent: string) => void;
}) {
  const { tr } = useLanguage();
  return (
    <>
      <button
        className="text-button"
        disabled={!wish.wishlist_id}
        onClick={() => edit(wish.wishlist_id!)}
      >
        <Pencil size={16} />
        {tr("Edit wish")}
      </button>
      <button
        className="text-button danger"
        disabled={!wish.wishlist_id}
        onClick={() => remove(wish.wishlist_id!)}
      >
        <Trash2 size={16} />
        {tr("Delete wish")}
      </button>
    </>
  );
}

function WishDetail({
  wish,
  initial,
  openCurrent,
  reservationId,
  signedIn,
  share,
  refresh,
  notify,
}: {
  wish: Wish;
  initial: Activity;
  openCurrent: () => void;
  reservationId?: number;
  signedIn: boolean;
  share: () => void;
  refresh: () => void;
  notify: (s: string) => void;
}) {
  const { tr, lang } = useLanguage();
  const [stats, setStats] = useState(initial);
  const [busy, setBusy] = useState(false);
  const [liking, setLiking] = useState(false);
  const [error, setError] = useState<unknown>(null);
  const [reserving, setReserving] = useState(false);
  const historical = !!reservationId && reservationId !== stats.reservation_id;
  const actions = historical ? [] : giftActions(stats);
  const stage = ["reserved", "purchased", "received"].indexOf(stats.status);
  async function reserve(plan: GiftPlan) {
    setBusy(true);
    setError(null);
    try {
      const gift = await request<GiftRecord>(`wish/${wish.id}/reservation/`, {
        method: "POST",
        body: { ...plan, ...(!signedIn ? { guest_key: guestKey() } : {}) },
        public: !signedIn,
        headers: giftHeaders(wish.id),
      });
      rememberGift(gift);
      setStats(await getActivity(wish.id));
      setReserving(false);
      notify(tr("Your plan is saved. A little thought, a real next step."));
      refresh();
    } catch (err) {
      setError(err);
      if (err instanceof ApiError && err.status === 409) {
        getActivity(wish.id)
          .then(setStats)
          .catch(() => {});
      }
    } finally {
      setBusy(false);
    }
  }
  async function change(action: "purchase" | "cancel" | "receive") {
    setBusy(true);
    setError(null);
    try {
      const gift = await request<GiftRecord>(`wish/${wish.id}/reservation/`, {
        method: "PATCH",
        body: { action },
        headers: giftHeaders(wish.id),
      });
      if (stats.is_giver) rememberGift(gift);
      setStats(await getActivity(wish.id));
      notify(
        action === "receive"
          ? tr(
              "Gift received. Your private check-in and shared notes are separate.",
            )
          : action === "cancel"
            ? tr("Reservation released. Another friend can pick it up.")
            : tr("Lovely! The owner can confirm when it arrives."),
      );
      refresh();
    } catch (err) {
      setError(err);
    } finally {
      setBusy(false);
    }
  }
  return (
    <section className="wish-detail">
      <Cover item={wish} />
      <div className="wish-detail-content">
        <span className="eyebrow">
          {stats.is_owner
            ? tr("YOUR LITTLE WISH")
            : tr("A LITTLE THOUGHT. A BIG SMILE.")}
        </span>
        <h1 dir="auto">{wish.name}</h1>
        <div className="wish-stats">
          <button
            className={`like-button ${stats.liked ? "liked" : ""}`}
            aria-pressed={stats.liked}
            disabled={liking}
            onClick={async () => {
              setLiking(true);
              setError(null);
              try {
                setStats(
                  await getActivity(wish.id, stats.liked ? "unlike" : "like"),
                );
              } catch (err) {
                setError(err);
              } finally {
                setLiking(false);
              }
            }}
          >
            <Heart size={21} fill={stats.liked ? "currentColor" : "none"} />
            {stats.likes} {stats.likes === 1 ? tr("like") : tr("likes")}
          </button>
          <span>
            <Eye size={21} />
            {stats.views} {stats.views === 1 ? tr("view") : tr("views")}
          </span>
          <button
            className="icon-button"
            onClick={share}
            aria-label={tr("Share wish")}
          >
            <Share2 size={21} />
          </button>
        </div>
        <p className="detail-description">
          {wish.description ||
            tr(
              "One of those things that would make an ordinary day a little better.",
            )}
        </p>
        <div className="detail-price">
          <strong>{money(wish.price, lang)}</strong>
          <span>{tr("Estimated price · in the owner’s currency")}</span>
        </div>
        <span className={`status status-${stats.status}`}>
          {tr(statusLabels[stats.status])}
        </span>
        {stage >= 0 && (
          <ol className="gift-progress" aria-label={tr("Gift progress")}>
            {[tr("Reserved"), tr("Bought"), tr("Received")].map(
              (label, index) => (
                <li key={label} className={stage >= index ? "complete" : ""}>
                  <span>
                    {stage >= index ? <Check size={15} /> : index + 1}
                  </span>
                  {label}
                </li>
              ),
            )}
          </ol>
        )}
        <div className="gift-action-box">
          {historical ? (
            <>
              <h2>{tr("A previous gift plan.")}</h2>
              <p>
                {tr(
                  "The private journey below belongs to that plan. Open the current wish to see its availability and next steps.",
                )}
              </p>
              <button className="button secondary full" onClick={openCurrent}>
                {tr("View current wish")}
                <ArrowRight className="directional" size={18} />
              </button>
            </>
          ) : stats.status === "received" ? (
            <>
              <Sparkles size={26} />
              <h2>{tr("A thoughtful gift, received.")}</h2>
              <p>
                {tr(
                  "The recipient confirmed it arrived. That’s a real moment to keep.",
                )}
              </p>
            </>
          ) : stats.is_owner ? (
            <>
              <h2>
                {stats.status === "available"
                  ? tr("Your next happy surprise.")
                  : stats.status === "reserved"
                    ? tr("Someone has their eye on this.")
                    : tr("A little joy is on its way.")}
              </h2>
              <p>
                {stats.status === "available"
                  ? tr("Share your wish with a friend who could use a hint.")
                  : stats.status === "reserved"
                    ? tr(
                        "A friend reserved this wish. We’ll let you know when they’ve bought it.",
                      )
                    : tr(
                        "When your gift arrives, confirm below to close the loop and thank your friend.",
                      )}
              </p>
              {stats.status === "available" && (
                <button className="button primary full" onClick={share}>
                  <Share2 size={18} />
                  {tr("Share this wish")}
                </button>
              )}
            </>
          ) : stats.is_giver ? (
            <>
              <h2>
                {stats.status === "reserved"
                  ? tr("This one’s yours to make happen.")
                  : tr("You’re about to make their day.")}
              </h2>
              <p>
                {stats.status === "reserved"
                  ? tr(
                      "Buy it wherever you like, then let them know it’s on the way.",
                    )
                  : tr(
                      "All set. The owner will confirm when your gift arrives.",
                    )}
              </p>
            </>
          ) : stats.status === "available" ? (
            <>
              <h2>{tr("Make their day.")}</h2>
              <p>{tr("Reserve this wish so no one buys the same gift.")}</p>
              <button
                className="button primary full"
                onClick={() => setReserving(true)}
              >
                <Gift size={20} />
                {tr("I’ll gift this")}
                <ArrowRight className="directional" size={19} />
              </button>
              <small>
                {tr("No payment here. You choose where to buy it.")}
              </small>
            </>
          ) : (
            <>
              <h2>{tr("A friend is on it.")}</h2>
              <p>
                {tr(
                  "This wish is already reserved. There are more thoughtful gifts waiting in their wishlist.",
                )}
              </p>
            </>
          )}
          {actions.map((action) => (
            <button
              key={action}
              disabled={busy}
              className={`button full ${action === "cancel" ? "text-button" : "primary"}`}
              onClick={() => {
                if (action === "cancel") setReserving(true);
                else change(action);
              }}
            >
              {busy ? (
                <LoaderCircle size={19} className="spin" />
              ) : (
                <Check size={19} />
              )}
              {action === "purchase"
                ? tr("I’ve bought it")
                : action === "receive"
                  ? tr("Confirm gift arrived")
                  : tr("Cancel reservation")}
            </button>
          ))}
          <ErrorMessage error={error} />
        </div>
        <GiftJourney
          wishId={wish.id}
          reservationId={
            reservationId ||
            stats.reservation_id ||
            localGifts().find((gift) => gift.wish_id === wish.id)?.id
          }
          refresh={refresh}
          notify={notify}
        />
        {reserving && (
          <Modal
            title={
              stats.is_giver
                ? tr("Release this reservation?")
                : tr("A thoughtful gift starts here.")
            }
            close={() => {
              if (!busy) {
                setReserving(false);
                setError(null);
              }
            }}
          >
            {stats.is_giver ? (
              <>
                <p className="modal-copy">
                  {tr(
                    "This wish will be available for another friend. Only cancel if you’re no longer giving this gift.",
                  )}
                </p>
                <div className="form-actions">
                  <button
                    className="button secondary"
                    disabled={busy}
                    onClick={() => setReserving(false)}
                  >
                    {tr("Keep reservation")}
                  </button>
                  <button
                    className="button destructive"
                    disabled={busy}
                    onClick={() => change("cancel")}
                  >
                    {busy ? tr("Releasing…") : tr("Release it")}
                  </button>
                </div>
              </>
            ) : (
              <CommitmentForm
                wish={wish}
                signedIn={signedIn}
                busy={busy}
                reserve={reserve}
              />
            )}
            <ErrorMessage error={error} />
          </Modal>
        )}
      </div>
    </section>
  );
}
