"""Centralized semantic selectors for Planeta.ru draft automation.

Selectors are deliberately narrow. If Planeta.ru changes its editor markup and none
of these exact semantic selectors match, the browser adapter must return
``ui_changed`` instead of guessing a nearby control.
"""

TITLE_INPUT = '[data-testid="campaign-title"], input[name="title"]'
TARGET_INPUT = '[data-testid="campaign-target"], input[name="target"], input[name="target_amount"]'
SUMMARY_INPUT = '[data-testid="campaign-summary"], textarea[name="summary"]'
STORY_EDITOR = '[data-testid="campaign-story"], textarea[name="story"]'
SAVE_DRAFT_BUTTON = '[data-testid="save-draft"], button[name="save_draft"]'
SUBMIT_MODERATION_BUTTON = '[data-testid="submit-moderation"], button[name="submit_moderation"]'

# Confirmed current multi-step editor controls. Keep these separate from the
# legacy unions above so a partial new layout can never be mistaken for the old
# single-page form.
ABOUT_TITLE_INPUT = "#about-name"
ABOUT_SUMMARY_INPUT = "#about-project"
ABOUT_END_DATE_INPUT = 'input[placeholder="ДД.ММ.ГГГГ"]'
ABOUT_REGION_SELECT = "select#about-region"
ABOUT_STORY_EDITOR = (
    '[class*="about-details-module__richText___"][contenteditable="true"], '
    '[class*="about-details-module__richText___"] [contenteditable="true"]'
)
ASSET_FILE_INPUTS = 'input[type="file"]'
GOAL_INPUT = "#editor-goal"

REQUIRED_DRAFT_SELECTORS = {
    "title": TITLE_INPUT,
    "target": TARGET_INPUT,
    "summary": SUMMARY_INPUT,
    "story": STORY_EDITOR,
    "save": SAVE_DRAFT_BUTTON,
    "submit": SUBMIT_MODERATION_BUTTON,
}

LOGIN_PASSWORD_INPUT = 'input[type="password"]'
CAPTCHA_WIDGET = '[data-sitekey], iframe[src*="captcha" i], iframe[src*="recaptcha" i]'
