// @ts-nocheck

import { serve } from "https://deno.land/std@0.177.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

serve(async (req) => {
  try {
    if (req.method !== "POST") {
      return new Response("Method Not Allowed", { status: 405 });
    }

    const body = await req.json();

    const {
      user_id,
      heart_rate,
      bp_sys,
      bp_dia,
      spo2,
      temperature_c,
      age
    } = body;

    // 1️⃣ Call Python ML API
    const mlResponse = await fetch("https://pec-ml-api.onrender.com/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        heart_rate,
        bp_sys,
        bp_dia,
        spo2,
        temperature_c,
        age
      })
    });

    if (!mlResponse.ok) {
      return new Response(
        JSON.stringify({ error: "ML API failed" }),
        { status: 500 }
      );
    }

    const {
      predicted_blood_sugar,
      predicted_resp_rate
    } = await mlResponse.json();

    // 2️⃣ Create Supabase client
    const supabaseUrl = Deno.env.get("usiuspwueenoaczxlvfz");
    const serviceKey = Deno.env.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVzaXVzcHd1ZWVub2FjenhsdmZ6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NTQ2MzAxNCwiZXhwIjoyMDgxMDM5MDE0fQ.F-UOBx_GiD3GkUZUSbyfqLqL-K8s630bWTA2utZ7Gek");

    if (!supabaseUrl || !serviceKey) {
      return new Response(
        JSON.stringify({ error: "Missing Supabase env vars" }),
        { status: 500 }
      );
    }

    const supabase = createClient(supabaseUrl, serviceKey);

    // 3️⃣ Insert into predictions table
    const { error } = await supabase
      .from("predictions")
      .insert({
        user_id,
        heart_rate,
        bp_sys,
        bp_dia,
        spo2,
        temperature_c,
        age,
        predicted_blood_sugar,
        predicted_resp_rate
      });

    if (error) {
      return new Response(
        JSON.stringify({ error: error.message }),
        { status: 400 }
      );
    }

    // 4️⃣ Return response
    return new Response(
      JSON.stringify({
        predicted_blood_sugar,
        predicted_resp_rate
      }),
      { status: 200 }
    );

  } catch (err) {
    return new Response(
      JSON.stringify({ error: String(err) }),
      { status: 500 }
    );
  }
});
