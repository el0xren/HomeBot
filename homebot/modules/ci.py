from homebot import get_config
from homebot.logging import LOGE, LOGI, LOGD, LOGW
from homebot.modules_manager import register

# Module-specific imports
from homebot import bot_path
from importlib import import_module
import os.path

@register(commands=['ci'])
def ci(update, context):
	if str(update.message.from_user.id) not in get_config("CI_APPROVED_USER_IDS").split():
		update.message.reply_text("Error: You are not authorized to use CI function of this bot.\nAsk to who host this bot to add you to the authorized people list")
		LOGI("Access denied to user " + str(update.message.from_user.id))
		return
	LOGI("Access granted to user " + str(update.message.from_user.id))
	if get_config("CI_CHANNEL_ID") == "":
		update.message.reply_text("Error: CI channel or user ID not defined")
		LOGE("CI channel or user ID not defined")
		return
	project = update.message.text.split()[1]
	if not os.path.isfile(bot_path / "modules" / "ci_projects" / (project + ".py")):
		update.message.reply_text("Error: Project script not found")
		return
	project_module = import_module('homebot.modules.ci_projects.' + project, package="*")
	LOGI("CI workflow started, project: " + project)
	project_module.ci_build(update, context)
	LOGI("CI workflow finished, project: " + project)
