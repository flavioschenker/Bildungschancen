"use client"
import Link from 'next/link';
import { useState } from "react"
import { login } from '@/app/actions';
import { EyeIcon, EyeOffIcon } from "lucide-react"
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { InputGroup, InputGroupAddon, InputGroupInput } from "@/components/ui/input-group"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox";
import {
  Field,
  FieldContent,
  FieldError,
  FieldGroup,
  FieldLabel,
  FieldSet,
} from "@/components/ui/field"
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

export default function LoginForm() {
  const [showPassword, setShowPassword] = useState(false)

  return (
    <form action={login} className="w-full max-w-sm">
      <Card>
        <CardHeader>
          <CardTitle>Create Account</CardTitle>
          <CardDescription>
            Enter your credentials below to login to your account
          </CardDescription>
        </CardHeader>
        <CardContent>
          <FieldSet>
            <FieldGroup>
              <Field>
                <FieldLabel>Email address*</FieldLabel>
                <FieldContent>
                  <Input
                    name="email"
                    type="email"
                    placeholder="m@example.com"
                    required
                    />
                </FieldContent>
              </Field>
            </FieldGroup>
            <FieldGroup>
              <Field>
                <FieldLabel>Password*</FieldLabel>
                <FieldContent>
                  <InputGroup>
                    <InputGroupInput
                      name="password"
                      type={showPassword ? "text" : "password"}
                      placeholder="********"
                      required
                      />
                    <InputGroupAddon 
                      align="inline-end" 
                      onClick={() => setShowPassword(!showPassword)}
                      className="cursor-pointer"
                      >
                      {showPassword ? <EyeIcon className="h-4 w-4" /> : <EyeOffIcon className="h-4 w-4" />}
                    </InputGroupAddon>
                  </InputGroup>
                </FieldContent>
              </Field>
              <Field>
                <FieldContent className="flex flex-row items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Checkbox id="remember" name="remember" className="cursor-pointer"/>
                    <Label htmlFor="remember" className="text-sm font-normal text-muted-foreground">
                      Remember me
                    </Label>
                  </div>
                  <Button variant="link" className="p-0 font-normal h-auto" asChild>
                    <Link href="/forgot-password">Forgot password?</Link>
                  </Button>
                </FieldContent>
              </Field>
            </FieldGroup>
          </FieldSet>
        </CardContent>
        <CardFooter className="flex flex-col gap-4">
          <Button type="submit" className="w-full cursor-pointer">Sign In</Button>
          <div className="text-center text-sm text-muted-foreground">
            Don't have an account?{" "}
            <Link href="/signup" className="underline underline-offset-4 hover:text-primary">
              Sign Up
            </Link>
          </div>
        </CardFooter>
      </Card>
    </form>
  )
}