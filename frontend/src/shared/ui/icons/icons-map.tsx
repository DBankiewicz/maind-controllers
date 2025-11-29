import { JSX } from 'react';
import { IconName } from './icon-name';
import { MoreVerticalIcon } from './icons-components/more-vertical-icon';
import {
  ArrowUp,
  CheckIcon,
  ChevronDown,
  Pencil,
  Pin,
  PlusIcon,
} from 'lucide-react';

export const iconsMap: Record<IconName, JSX.Element> = {
  CHECK: <CheckIcon />,
  CHEVRON_DOWN: <ChevronDown />,
  MORE_VERTICAL: <MoreVerticalIcon />,
  PENCIL: <Pencil />,
  PIN: <Pin />,
  PLUS: <PlusIcon />,
  SHORT_ARROW_UP: <ArrowUp />,
};
