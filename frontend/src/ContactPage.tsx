import { useEffect, useState } from "react";
import { Mail } from "lucide-react";
import { request } from "./api";
import { Empty, ErrorMessage, Loading } from "./components";
import { useLanguage } from "./i18n";
export function ContactPage() {
  const { tr } = useLanguage();
  const [contacts, setContacts] = useState<
    { id: string; email: string }[] | null
  >(null);
  const [error, setError] = useState<unknown>(null);
  const [attempt, setAttempt] = useState(0);
  useEffect(() => {
    const controller = new AbortController();
    setError(null);
    setContacts(null);
    request<{ id: string; email: string }[]>("website/contact-us/", {
      public: true,
      signal: controller.signal,
    })
      .then(setContacts)
      .catch((e) => {
        if (!controller.signal.aborted) {
          if (e.status === 404) setContacts([]);
          else setError(e);
        }
      });
    return () => controller.abort();
  }, [attempt]);
  return (
    <section className="narrow">
      <div className="page-heading">
        <span className="eyebrow">{tr("Contact & support")}</span>
        <h1>{tr("Need a hand?")}</h1>
        <p>{tr("Here’s how to reach the Wishy team.")}</p>
      </div>
      {error ? (
        <>
          <ErrorMessage error={error} />
          <button
            className="button secondary"
            onClick={() => setAttempt((n) => n + 1)}
          >
            {tr("Try again")}
          </button>
        </>
      ) : contacts === null ? (
        <Loading />
      ) : contacts.length ? (
        <div className="panel contact-links">
          {contacts.map((contact) => (
            <a
              className="button secondary"
              key={contact.id}
              href={`mailto:${contact.email}`}
            >
              <Mail size={18} />
              <bdi dir="ltr">{contact.email}</bdi>
            </a>
          ))}
        </div>
      ) : (
        <Empty
          title={tr("Contact & support")}
          copy={tr("No contact details have been published yet.")}
        />
      )}
    </section>
  );
}
