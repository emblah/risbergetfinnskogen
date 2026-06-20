# Archived Form Mail

These files were moved out of `risbergetvaalerfinnskog.com/onewebstatic/` so the static website no longer carries the One.com form mail integration by default.

- `6b43a23c09.js` initializes the contact form and contains the One.com `oneconnect.one.com/form-mail` post URL.
- `07e4829d26.js` contains the One.com contact form runtime.

The contact page is `../risbergetvaalerfinnskog.com/118111338.html`.

To restore the integration, run:

```bash
./restore-form-mail.sh
```
