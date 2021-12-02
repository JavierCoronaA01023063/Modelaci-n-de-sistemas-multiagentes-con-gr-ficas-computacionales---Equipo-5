using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class Agents
{
    public List<Vector3> positions;
}
public class AgentController : MonoBehaviour
{
    [SerializeField] string url;
    [SerializeField] string testEP;
    [SerializeField] string configEP;
    [SerializeField] private string updateEP;
    [SerializeField] private string updateOrganizingAgentsEP;
    [SerializeField] private string updateBoxAgentsEP;
    [SerializeField] int numAgents;
    [SerializeField] int numBoxes;
    [SerializeField] int width;
    [SerializeField] int height;
    [SerializeField] private GameObject organizingAgentPrefab;
    [SerializeField] private GameObject boxAgentPrefab;
    [SerializeField] private float timeToUpdate;
    [SerializeField] GameObject floor;

    Agents oAgents, bAgents;
    GameObject[] organizingAgents, boxAgents;
    private float updateTime = 0;
    
    List<Vector3> oldPosOrg;
    List<Vector3> newPosOrg;
    List<Vector3> oldPosBox;
    List<Vector3> newPosBox;
    
    float timer, dt;
    
    // Pause the simulation while we get the update from the server
    bool hold = false;

    // Start is called before the first frame update
    void Start()
    {
        oldPosOrg = new List<Vector3>();
        newPosOrg = new List<Vector3>();
        oldPosBox = new List<Vector3>();
        newPosBox = new List<Vector3>();
        
        organizingAgents = new GameObject[numAgents];
        boxAgents = new GameObject[numBoxes];

        floor.transform.localScale = new Vector3((float) width / 10, 1, (float) height / 10);
        floor.transform.localPosition = new Vector3((float) width / 2 - 0.5f, 0, (float) height / 2 - 0.5f);

        timer = timeToUpdate;
        
        for (int i = 0; i < numAgents; i++)
        {
            organizingAgents[i] = Instantiate(organizingAgentPrefab, Vector3.up, Quaternion.identity);
        }
        
        for (int i = 0; i < numBoxes; i++)
        {
            boxAgents[i] = Instantiate(boxAgentPrefab, Vector3.up, Quaternion.identity);
        }
        
        StartCoroutine(SendConfig()); 
    }

    // Update is called once per frame
    void Update()
    {
        float t = timer / timeToUpdate;

        dt = t * t * (3f - 2f * t);
        
        if(timer >= timeToUpdate)
        {
            timer = 0;
            hold = true;
            StartCoroutine(UpdateSimulation());
        }
        
        if (!hold)
        {
            MoveOrganizingAgents();
            MoveBoxAgent();
            // Move time from the last frame
            timer += Time.deltaTime;
        }
    }

    IEnumerator TestAPI()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + testEP);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success)
        {
            Debug.Log(www.downloadHandler.text);
        }
        else
        {
            Debug.Log(www.error);
        }
    }
    
    IEnumerator SendConfig()
    {
        WWWForm form = new WWWForm();
        form.AddField("numAgents", numAgents.ToString());
        form.AddField("numBoxes", numBoxes.ToString());
        form.AddField("width", width.ToString());
        form.AddField("height", height.ToString());
        
        UnityWebRequest www = UnityWebRequest.Post(url + configEP, form);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success)
        {
            StartCoroutine(GetOrganizingData());
            StartCoroutine(GetBoxData());
        }
        else
        {
            Debug.Log(www.error);
        }
    }
    
    IEnumerator UpdateSimulation()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + updateEP);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            StartCoroutine(GetOrganizingData());
            StartCoroutine(GetBoxData());
        }
    }

    IEnumerator GetOrganizingData()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + updateOrganizingAgentsEP);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        { 
            oAgents = JsonUtility.FromJson<Agents>(www.downloadHandler.text);
            
            oldPosOrg = new List<Vector3>(newPosOrg);

            newPosOrg.Clear();

            foreach(Vector3 v in oAgents.positions)
                newPosOrg.Add(v);

            hold = false;
        }
    }
    
    IEnumerator GetBoxData()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + updateBoxAgentsEP);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            bAgents = JsonUtility.FromJson<Agents>(www.downloadHandler.text);
            
            oldPosBox = new List<Vector3>(newPosBox);

            newPosBox.Clear();

            foreach(Vector3 v in bAgents.positions)
                newPosBox.Add(v);

            hold = false;
        }
    }

    void MoveOrganizingAgents()
    {
        Debug.Log(oldPosOrg[0] + " Size Test");
        for (int i = 0; i < numAgents; i++)
        {
            Vector3 interpolated = Vector3.Lerp(oldPosOrg[i], newPosOrg[i], dt);
            organizingAgents[i].transform.localPosition = interpolated;
                
            Vector3 dir = oldPosOrg[i] - newPosOrg[i];
            organizingAgents[i].transform.rotation = Quaternion.LookRotation(dir);
        }
    }

    void MoveBoxAgent()
    {
        for (int i = 0; i < numBoxes; i++)
        {
            Vector3 interpolated = Vector3.Lerp(oldPosBox[i], newPosBox[i], dt);
            boxAgents[i].transform.localPosition = interpolated;
                
            Vector3 dir = oldPosBox[i] - newPosBox[i];
            boxAgents[i].transform.rotation = Quaternion.LookRotation(dir);
        }
    }
}
