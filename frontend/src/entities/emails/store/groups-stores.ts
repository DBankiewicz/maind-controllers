import { createStore } from "effector";
import { EmailsGroupDto } from "../types";
import { fetchUserGroupsFx } from "./effects";

export const $groups = createStore<EmailsGroupDto[]>([]);

$groups
  .on(fetchUserGroupsFx.doneData, (_, groups) => groups);
