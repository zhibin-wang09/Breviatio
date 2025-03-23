# Guideline and Explanations

## `auth.py`

`auth.py` is the bridge for us to set up authorization and authentication with the google api
so we can further use google's resources

Flow of OAuth 2.0
1. Brevatio identifies the permission it needs
2. The application redirects the user to Google along with the list of requested permissions
3. The user decides whether to grant the permissions to Brevatio
4. Brevatio finds out what the user decided
5. If the user granted the requested permissions, Brevatio retrieves token needed to make API requests on the user's behalf