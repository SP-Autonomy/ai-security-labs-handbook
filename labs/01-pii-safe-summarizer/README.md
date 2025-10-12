## 🧪 Test Scenarios
Test Matrix
<table>
<thead>
<tr>
<th width="25%">Scenario</th>
<th width="15%">Role</th>
<th width="15%">Clearance</th>
<th width="15%">Has PII</th>
<th width="15%">Has Injection</th>
<th width="15%">Expected</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Test 1</strong><br/>Malicious + Contractor</td>
<td>contractor</td>
<td>-</td>
<td>✅ Yes</td>
<td>✅ Yes</td>
<td>❌ BLOCKED<br/><code>prompt_injection_suspected</code></td>
</tr>
<tr>
<td><strong>Test 2</strong><br/>Benign + Employee</td>
<td>employee</td>
<td>-</td>
<td>❌ No</td>
<td>❌ No</td>
<td>✅ SUCCESS</td>
</tr>
<tr>
<td><strong>Test 3</strong><br/>Sensitive Information + Regular Employee</td>
<td>employee</td>
<td>none</td>
<td>✅ Yes</td>
<td>❌ No</td>
<td>❌ BLOCKED<br/><code>policy_denied</code></td>
</tr>
<tr>
<td><strong>Test 4</strong><br/>Sensitive Information + Approved Employee</td>
<td>employee</td>
<td>pii_approved</td>
<td>✅ Yes</td>
<td>❌ No</td>
<td>✅ SUCCESS with PII masked</td>
</tr>
</tbody>
</table>

## Expected Results
<details>
<summary><b>❌ Test 1: BLOCKED - Malicious Contractor</b></summary>
  <img width="1029" height="620" alt="Malicious Contractor Prompt" src="https://github.com/user-attachments/assets/5f6bb24d-76cc-4382-88bb-d431c1701db7" />
</details>
<details><summary><b>✅ Test 2: SUCCESS - Benign Employee</b></summary>
  <img width="1360" height="1707" alt="Benign Employee Prompt" src="https://github.com/user-attachments/assets/858f597e-1abb-4a82-95ae-2fdc7e9a61c5" />
</details>
<details><summary><b>❌ Test 3: BLOCKED - Sensitive Information + Regular Employee</b></summary>
  <img width="1119" height="752" alt="Regular Employee Sensitive Content Prompt" src="https://github.com/user-attachments/assets/2b30503d-6048-41ec-aa0e-181ac8fd9fa9" />
</details>
<details><summary><b>✅ Test 4: SUCCESS - Sensitive Information + Approved Employee</b></summary>
  <img width="1360" height="1771" alt="Approved Employee Sensitive Content Prompt" src="https://github.com/user-attachments/assets/5a5ea220-6b08-4c13-a74d-9edc0509fdb8" />
</details>
