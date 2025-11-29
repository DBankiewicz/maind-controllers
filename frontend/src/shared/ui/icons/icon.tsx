import { IconName } from './icon-name';
import { iconsMap } from './icons-map';
import classNames from 'classnames';
import './icon.css';

type IconProps = {
  icon: IconName;
  className?: string | string[];
  onClick?: (event: React.MouseEvent) => void;
};

export function Icon({ icon, className, onClick }: IconProps) {
  const iconComponent = iconsMap[icon];

  return (
    <div className={classNames('icon-container', className)} onClick={onClick}>
      {iconComponent}
    </div>
  );
}
