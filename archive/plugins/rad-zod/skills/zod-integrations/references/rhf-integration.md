# React Hook Form + Zod Integration Reference

## Installation

```bash
npm install react-hook-form @hookform/resolvers zod
```

## Basic Pattern

```typescript
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const LoginSchema = z.object({
  email: z.email({ error: "Enter a valid email address" }),
  password: z.string().min(8, { error: "Password must be at least 8 characters" }),
  rememberMe: z.boolean().default(false),
});
type LoginForm = z.infer<typeof LoginSchema>;

function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginForm>({
    resolver: zodResolver(LoginSchema),
    defaultValues: { email: "", password: "", rememberMe: false },
  });

  const onSubmit = handleSubmit(async (data) => {
    // data is typed as LoginForm
    await authService.login(data);
  });

  return (
    <form onSubmit={onSubmit}>
      <input {...register("email")} type="email" />
      {errors.email && <span>{errors.email.message}</span>}

      <input {...register("password")} type="password" />
      {errors.password && <span>{errors.password.message}</span>}

      <input {...register("rememberMe")} type="checkbox" />

      <button type="submit" disabled={isSubmitting}>Sign In</button>
    </form>
  );
}
```

## Coercion Patterns for HTML Inputs

HTML inputs always return strings. Use coercion for numeric and date fields:

```typescript
const ProductFormSchema = z.object({
  name: z.string().min(1),
  price: z.coerce.number().positive({ error: "Price must be positive" }),
  stock: z.coerce.number().int().min(0),
  weight: z.coerce.number().positive().optional(),
  launchDate: z.coerce.date().refine(d => !isNaN(d.getTime()), "Invalid date"),
  isActive: z.coerce.boolean(), // "true"/"false" string from select
});

// For <select> that returns "true"/"false" string:
const BooleanSelectSchema = z.string()
  .refine(s => s === "true" || s === "false")
  .transform(s => s === "true");
```

## File Upload Validation

```typescript
const UploadSchema = z.object({
  title: z.string().min(1),
  avatar: z.instanceof(File, { message: "Please select a file" })
    .refine(f => f.size <= 5 * 1024 * 1024, "File must be under 5MB")
    .refine(
      f => ["image/jpeg", "image/png", "image/webp"].includes(f.type),
      "File must be JPEG, PNG, or WebP"
    ),
  // Or use Zod 4's built-in (browser environment only):
  // avatar: z.file().max(5 * 1024 * 1024).type("image/jpeg", "image/png", "image/webp"),
});

// Register file input — must use setValue, not register directly
function AvatarUpload() {
  const { setValue, watch } = useFormContext();
  const avatar = watch("avatar");

  return (
    <input
      type="file"
      accept="image/jpeg,image/png,image/webp"
      onChange={e => setValue("avatar", e.target.files?.[0], { shouldValidate: true })}
    />
  );
}
```

## The Create/Edit Form Hook Pattern

Eliminates schema duplication between create and edit modes:

```typescript
// The base schema — used for both modes
const UserFormSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.email(),
  role: z.enum(["admin", "user", "moderator"]),
  bio: z.string().max(500).optional(),
});
type UserFormData = z.infer<typeof UserFormSchema>;

// Custom hook handles both modes
function useUserForm(existingUser?: User) {
  return useForm<UserFormData>({
    resolver: zodResolver(UserFormSchema),
    defaultValues: existingUser
      ? {
          name: existingUser.name,
          email: existingUser.email,
          role: existingUser.role,
          bio: existingUser.bio ?? "",
        }
      : {
          name: "",
          email: "",
          role: "user",
          bio: "",
        },
  });
}

// Create page
function CreateUserPage() {
  const form = useUserForm(); // No initial data
  return <UserFormUI form={form} onSubmit={createUser} />;
}

// Edit page
function EditUserPage({ user }: { user: User }) {
  const form = useUserForm(user); // Pre-populated
  return <UserFormUI form={form} onSubmit={updateUser} />;
}
```

## Multi-Step Form Pattern

```typescript
// Step-specific schemas
const Step1Schema = z.object({
  firstName: z.string().min(1),
  lastName: z.string().min(1),
  birthdate: z.coerce.date(),
});

const Step2Schema = z.object({
  email: z.email(),
  phone: z.string().regex(/^\+?[\d\s()-]{10,}$/),
});

const Step3Schema = z.object({
  address: z.string().min(5),
  city: z.string().min(1),
  zip: z.string().regex(/^\d{5}(-\d{4})?$/),
});

// Combined schema for final submission
const FullRegistrationSchema = Step1Schema.merge(Step2Schema).merge(Step3Schema);
type FullRegistration = z.infer<typeof FullRegistrationSchema>;

// Component: use FormProvider to share form state across steps
function RegistrationWizard() {
  const [step, setStep] = React.useState(1);
  const methods = useForm<FullRegistration>({
    resolver: zodResolver(FullRegistrationSchema),
    mode: "onTouched",
  });

  return (
    <FormProvider {...methods}>
      <form onSubmit={methods.handleSubmit(submitRegistration)}>
        {step === 1 && <Step1 onNext={() => setStep(2)} />}
        {step === 2 && <Step2 onBack={() => setStep(1)} onNext={() => setStep(3)} />}
        {step === 3 && <Step3 onBack={() => setStep(2)} />}
      </form>
    </FormProvider>
  );
}

// Step components use useFormContext() — no prop drilling
function Step1({ onNext }: { onNext: () => void }) {
  const { register, trigger, formState: { errors } } = useFormContext<FullRegistration>();

  const handleNext = async () => {
    // Validate only step 1 fields before advancing
    const valid = await trigger(["firstName", "lastName", "birthdate"]);
    if (valid) onNext();
  };

  return (
    <div>
      <input {...register("firstName")} />
      {errors.firstName && <span>{errors.firstName.message}</span>}
      <button type="button" onClick={handleNext}>Next</button>
    </div>
  );
}
```

## Cross-Field Validation

```typescript
const PasswordResetSchema = z.object({
  newPassword: z.string().min(12),
  confirmPassword: z.string(),
}).refine(
  data => data.newPassword === data.confirmPassword,
  {
    message: "Passwords do not match",
    path: ["confirmPassword"], // Error shown on confirmPassword field
  }
);

// Access root-level refine errors:
const { formState: { errors } } = useForm({ resolver: zodResolver(PasswordResetSchema) });
// errors.confirmPassword.message — "Passwords do not match"
// errors.root — for form-level errors (path: [])
```
