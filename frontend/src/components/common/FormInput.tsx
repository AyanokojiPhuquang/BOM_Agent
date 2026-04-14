import type { InputHTMLAttributes, SelectHTMLAttributes, ReactNode } from 'react';
import { cn } from '@/utils/cn';
import { INPUT_CLASS } from '@/constants';

interface BaseProps {
  label: string;
  className?: string;
}

type InputProps = BaseProps &
  Omit<InputHTMLAttributes<HTMLInputElement>, 'className'> & {
    as?: 'input';
  };

type SelectProps = BaseProps &
  Omit<SelectHTMLAttributes<HTMLSelectElement>, 'className'> & {
    as: 'select';
    children: ReactNode;
  };

type FormInputProps = InputProps | SelectProps;

export function FormInput(props: FormInputProps) {
  const { label, className, as = 'input', ...rest } = props;

  return (
    <div>
      <label className="block text-sm text-gray-400 mb-1">{label}</label>
      {as === 'select' ? (
        <select
          className={cn(INPUT_CLASS, className)}
          {...(rest as Omit<SelectHTMLAttributes<HTMLSelectElement>, 'className'>)}
        >
          {(props as SelectProps).children}
        </select>
      ) : (
        <input
          className={cn(INPUT_CLASS, className)}
          {...(rest as Omit<InputHTMLAttributes<HTMLInputElement>, 'className'>)}
        />
      )}
    </div>
  );
}
