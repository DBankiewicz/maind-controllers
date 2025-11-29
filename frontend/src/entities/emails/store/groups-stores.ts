import { createStore } from "effector";
import { EmailsGroupDto } from "../types";
import { fetchUserGroupsFx } from "./effects";

const $emailsGroups = createStore<EmailsGroupDto[]>([]);

$emailsGroups
  .on(fetchUserGroupsFx.doneData, (_, groups) => groups);
